from typing import Dict
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from bank_api.middlewares.auth import jwt_bearer_middleware
from bank_api.ports.payment_account_service_interface import \
    PaymentAccountServiceInterface
from bank_api.schemas.payment_account_schemas import GetStatementFilters


class PaymentAccountController:
    def __init__(
        self,
        service: PaymentAccountServiceInterface,
    ):
        self.service = service
        self.router = APIRouter()

        self.router.add_api_route(
            '/balance/{payment_account_id}',
            self.__get_balance,
            methods=['GET'],
            status_code=200,
        )

        self.router.add_api_route(
            '/{account_id}/statements',
            self.__get_statements,
            methods=['GET'],
            status_code=200,
        )

    async def __get_balance(
        self,
        payment_account_id: UUID,
        token_data: Dict = Depends(jwt_bearer_middleware)
    ):
        return await self.service.get_balance(payment_account_id)

    async def __get_statements(
        self,
        account_id: UUID,
        start: str | None = Query(None),
        end: str | None = Query(None),
        page: int | None = Query(1),
        limit: int | None = Query(10),
        token_data: Dict = Depends(jwt_bearer_middleware)
    ):
        filters = GetStatementFilters(start=start, end=end, page=page, limit=limit)
        return await self.service.statement(account_id, filters)
