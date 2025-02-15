from fastapi import APIRouter

from bank_api.ports.auth_service_interface import AuthServiceInterface
from bank_api.schemas.auth_schemas import AuthInput


class AuthController:
    def __init__(
        self,
        service: AuthServiceInterface,
    ):
        self.service = service
        self.router = APIRouter()

        self.router.add_api_route(
            '/',
            self.__auth,
            methods=['POST'],
            status_code=200,
        )

    async def __auth(
        self,
        params: AuthInput,
    ):
        return await self.service.authenticate(username=params.username, password=params.password)
