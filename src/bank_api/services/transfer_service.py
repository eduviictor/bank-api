from http import HTTPStatus

from bank_api.exceptions.http_exceptions import HttpException
from bank_api.exceptions.payment_account_exceptions import \
    PaymentAccountException
from bank_api.ports.transfer_service_interface import TransferServiceInterface
from bank_api.schemas.payment_account_schemas import GetBalanceOutput
from bank_api.schemas.transfer_schemas import CreateTransferInput


class TransferService(TransferServiceInterface):
    async def transfer(self, params: CreateTransferInput):
        sender_account = await self.payment_account_repository.find_by_id(params.sender_account_id)
        receiver_account = await self.payment_account_repository.find_by_id(params.receiver_account_id)

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
