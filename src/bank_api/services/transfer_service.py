from http import HTTPStatus

from bank_api.exceptions.http_exceptions import HttpException
from bank_api.exceptions.payment_account_exceptions import \
    PaymentAccountException
from bank_api.ports.transfer_service_interface import TransferServiceInterface
from bank_api.schemas.transfer_schemas import (CreateTransferInput,
                                               CreateTransferOutput,
                                               MoveInternalFoundsInput,
                                               MoveInternalFoundsOutput,
                                               MoveInternalFoundsType)
from bank_api.utils.log import logger
from config.database.models.payment_account import (PaymentAccount,
                                                    PaymentAccountType)
from config.database.models.transaction import TransactionDetailType


class TransferService(TransferServiceInterface):
    async def transfer(self, params: CreateTransferInput):
        sender_account = await self.payment_account_repository.find(id=params.sender_account_id)
        receiver_account = await self.payment_account_repository.find(id=params.receiver_account_id)

        if not sender_account or not receiver_account:
            raise HttpException(code=HTTPStatus.NOT_FOUND, message='Account not found')

        if sender_account.id == receiver_account.id:
            raise HttpException(code=HTTPStatus.BAD_REQUEST, message='Sender and receiver accounts must be different')

        if sender_account.balance < params.amount:
            raise HttpException(code=HTTPStatus.BAD_REQUEST, message='Insufficient funds')

        try:
            result = await self.payment_account_repository.transfer(sender_account, receiver_account, params.amount, TransactionDetailType.TRANSFER)
            return CreateTransferOutput(balance=sender_account.balance, transaction_id=result.debit_transaction_id)
        except PaymentAccountException as exc:
            raise HttpException(code=HTTPStatus.BAD_REQUEST, message=str(exc))
        except Exception as exc:
            raise HttpException(code=HTTPStatus.INTERNAL_SERVER_ERROR, message=str(exc))

    async def move_internal_founds(self, params: MoveInternalFoundsInput):
        account = await self.payment_account_repository.find(id=params.account_id)

        if not account:
            raise HttpException(code=HTTPStatus.NOT_FOUND, message='Account not found')

        if account.balance < params.amount:
            raise HttpException(code=HTTPStatus.BAD_REQUEST, message='Insufficient funds')

        if account.account_type == PaymentAccountType.CHECKING:
            if params.type == MoveInternalFoundsType.INVESTMENT:
                raise HttpException(code=HTTPStatus.BAD_REQUEST, message='Cannot invest to a checking account')

            return await self.__process_move_founds(account, params.amount, TransactionDetailType.WITHDRAW_TRANSFER, PaymentAccountType.SAVINGS)

        else:
            if params.type == MoveInternalFoundsType.WITHDRAW:
                raise HttpException(code=HTTPStatus.BAD_REQUEST, message='Cannot withdraw from a savings account')

            return await self.__process_move_founds(account, params.amount, TransactionDetailType.INVESTMENT, PaymentAccountType.CHECKING)

    async def __process_move_founds(self, sender: PaymentAccount, amount: int, detail_type: TransactionDetailType, account_type: PaymentAccountType):
        account_receiver = await self.payment_account_repository.find(tax_id=sender.tax_id, account_type=account_type)
        logger.info(f'account_receiver: {account_receiver}')
        if not account_receiver:
            raise HttpException(code=HTTPStatus.NOT_FOUND, message='Account not found')

        try:
            await self.payment_account_repository.transfer(
                sender=sender,
                receiver=account_receiver,
                amount=amount,
                detail_type=detail_type
            )
            return MoveInternalFoundsOutput(
                checking_balance=sender.balance if sender.account_type == PaymentAccountType.CHECKING else account_receiver.balance,
                savings_balance=sender.balance if sender.account_type == PaymentAccountType.SAVINGS else account_receiver.balance,
            )
        except PaymentAccountException as exc:
            raise HttpException(code=HTTPStatus.BAD_REQUEST, message=str(exc))
        except Exception as exc:
            raise HttpException(code=HTTPStatus.INTERNAL_SERVER_ERROR, message=str(exc))
