from abc import ABC, abstractmethod

from bank_api.ports.payment_account_repository_interface import \
    PaymentAccountRepositoryInterface
from bank_api.schemas.payment_account_schemas import GetBalanceOutput


class PaymentAccountServiceInterface(ABC):
    def __init__(
            self,
            payment_account_repository: PaymentAccountRepositoryInterface
        ):
        self.payment_account_repository = payment_account_repository

    @abstractmethod
    async def get_balance(self, payment_account_id: int) -> GetBalanceOutput:
        raise NotImplementedError

    @abstractmethod
    async def statement(self, payment_account_id: int):
        raise NotImplementedError
