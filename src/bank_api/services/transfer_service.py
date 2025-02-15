from http import HTTPStatus

from bank_api.exceptions.http_exceptions import HttpException
from bank_api.exceptions.payment_account_exceptions import \
    PaymentAccountException
from bank_api.ports.transfer_service_interface import TransferServiceInterface
from bank_api.schemas.payment_account_schemas import GetBalanceOutput
from bank_api.schemas.transfer_schemas import (CreateTransferInput,
                                               MoveInternalFoundsInput,
                                               MoveInternalFoundsType)
from config.database.models.payment_account import PaymentAccountType
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
            await self.payment_account_repository.transfer(sender_account, receiver_account, params.amount)
            return GetBalanceOutput(balance=sender_account.balance)
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

            account_receiver = await self.payment_account_repository.find(tax_id=account.tax_id, account_type=PaymentAccountType.SAVINGS)

            if not account_receiver:
                raise HttpException(code=HTTPStatus.NOT_FOUND, message='Savings account not found')
            detail_type = TransactionDetailType.WITHDRAW_TRANSFER

        if account.account_type == PaymentAccountType.SAVINGS:
            if params.type == MoveInternalFoundsType.WITHDRAW:
                raise HttpException(code=HTTPStatus.BAD_REQUEST, message='Cannot withdraw from a savings account')

            account_receiver = await self.payment_account_repository.find(tax_id=account.tax_id, account_type=PaymentAccountType.CHECKING)

            if not account_receiver:
                raise HttpException(code=HTTPStatus.NOT_FOUND, message='Checking account not found')
            detail_type = TransactionDetailType.INVESTMENT

        try:
            await self.payment_account_repository.transfer(
                sender=account,
                receiver=account_receiver,
                amount=params.amount,
                detail_type=detail_type
            )
            return GetBalanceOutput(balance=account.balance)
        except PaymentAccountException as exc:
            raise HttpException(code=HTTPStatus.BAD_REQUEST, message=str(exc))
        except Exception as exc:
            raise HttpException(code=HTTPStatus.INTERNAL_SERVER_ERROR, message=str(exc))
