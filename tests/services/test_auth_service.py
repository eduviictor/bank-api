# pylint: disable=too-many-lines

from unittest.mock import AsyncMock, patch
from uuid import uuid4

from pytest import fixture, raises

from bank_api.exceptions.http_exceptions import HttpException
from bank_api.services.auth_service import AuthService
from config.database.models.user import User


class TestAuthService:
    @fixture(autouse=True)
    def setup(self):
        self.user_repository = AsyncMock()
        self.auth_adapter = AsyncMock()

        self.service = AuthService(
            auth_adapter=self.auth_adapter,
            user_repository=self.user_repository
        )

    @fixture(name='user')
    def user(self):
        return User(
            id=uuid4().hex,
            username='username',
            password=uuid4().hex,
            created_at='2021-01-01',
            updated_at='2021-01-01',
        )

    async def test_authenticate_raises_unauthorized_when_user_not_found(self, user):
        self.user_repository.get_by_username.return_value = None
        self.auth_adapter.generate_token = AsyncMock()

        with raises(HttpException) as context:
            await self.service.authenticate(user.username, user.password)

        assert context.value.code == 401

    async def test_authenticate_raises_unauthorized_when_password_does_not_match(self, user):
        self.user_repository.get_by_username.return_value = user
        self.auth_adapter.generate_token = AsyncMock()
        with patch('bcrypt.checkpw', return_value=False):
            with raises(HttpException) as context:
                await self.service.authenticate(user.username, user.password)

            assert context.value.code == 401

    async def test_authenticate_returns_access_token(self, user):
        self.user_repository.get_by_username.return_value = user
        self.auth_adapter.generate_token = AsyncMock()

        with patch('bcrypt.checkpw', return_value=True):
            response = await self.service.authenticate(user.username, user.password)

        assert 'access_token' in response
        self.auth_adapter.generate_token.assert_called_once_with(
            username=user.username,
            expires_in=3600,
        )
