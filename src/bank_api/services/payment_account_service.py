from http import HTTPStatus

from bank_api.exceptions.http_exceptions import HttpException
from datetime import datetime
from bank_api.ports.payment_account_service_interface import \
    PaymentAccountServiceInterface
from bank_api.schemas.payment_account_schemas import (GetBalanceOutput,
                                                      GetStatementFilters)


class PaymentAccountService(PaymentAccountServiceInterface):
    async def get_balance(self, payment_account_id: str) -> GetBalanceOutput:
        account = await self.payment_account_repository.find(id=payment_account_id)
        if not account:
            raise HttpException(message='Account not found', code=HTTPStatus.NOT_FOUND)
        return GetBalanceOutput(balance=account.balance)

    async def statement(self, payment_account_id: str, filters: GetStatementFilters):
        account = await self.payment_account_repository.find(id=payment_account_id)
        if not account:
            raise HttpException(message='Account not found', code=HTTPStatus.NOT_FOUND)

        if not filters.start:
            filters.start = int(datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0).timestamp())
        if not filters.end:
            filters.end = int(datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999).timestamp())

        return await self.payment_account_repository.statement(account.id, filters)
