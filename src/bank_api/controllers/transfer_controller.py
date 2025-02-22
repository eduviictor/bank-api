from typing import Dict

from fastapi import APIRouter, Depends

from bank_api.middlewares.auth import jwt_bearer_middleware
from bank_api.ports.transfer_service_interface import TransferServiceInterface
from bank_api.schemas.transfer_schemas import (CreateTransferInput,
                                               MoveInternalFoundsInput)


class TransferController:
    def __init__(
        self,
        service: TransferServiceInterface,
    ):
        self.service = service
        self.router = APIRouter()

        self.router.add_api_route(
            '',
            self.__transfer,
            methods=['POST'],
            status_code=200,
        )

        self.router.add_api_route(
            '/move-internal-founds',
            self.__move,
            methods=['POST'],
            status_code=200,
        )

    async def __transfer(
        self,
        params: CreateTransferInput,
        token_data: Dict = Depends(jwt_bearer_middleware)
    ):
        return await self.service.transfer(params)

    async def __move(
        self,
        params: MoveInternalFoundsInput,
        token_data: Dict = Depends(jwt_bearer_middleware)
    ):
        return await self.service.move_internal_founds(params)
