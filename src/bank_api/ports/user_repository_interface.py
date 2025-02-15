from abc import ABC, abstractmethod
from typing import List, Optional

from bank_api.ports.repository_interface import RepositoryInterface
from config.database.models import PaymentAccount
from config.database.models.user import User


class UserRepositoryInterface(RepositoryInterface, ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[PaymentAccount]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[PaymentAccount]:
        raise NotImplementedError

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError
