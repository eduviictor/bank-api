from http import HTTPStatus

from bank_api.exceptions.http_exceptions import HttpException
from bank_api.ports.auth_service_interface import AuthServiceInterface
from bank_api.utils.password import verify_password


class AuthService(AuthServiceInterface):
    async def authenticate(self, username: str, password: str) -> bool:
        user = await self.user_repository.get_by_username(username)

        if user and verify_password(password, user.password):
            access_token = self.auth_adapter.generate_token(
                username=user.username,
                expires_in=3600,
            )
            return {
                'access_token': access_token,
            }
        raise HttpException(message='Credenciais inválidas', code=HTTPStatus.UNAUTHORIZED)
