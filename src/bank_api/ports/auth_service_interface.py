from abc import ABC, abstractmethod

from bank_api.ports.auth_adapter_interface import AuthAdapterInterface
from bank_api.ports.user_repository_interface import UserRepositoryInterface


class AuthServiceInterface(ABC):
    def __init__(
        self,
        auth_adapter: AuthAdapterInterface,
        user_repository: UserRepositoryInterface
    ):
        self.auth_adapter = auth_adapter
        self.user_repository = user_repository

    @abstractmethod
    async def authenticate(self, username: str, password: str) -> bool:
        pass
