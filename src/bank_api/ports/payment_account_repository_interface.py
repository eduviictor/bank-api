from abc import ABC, abstractmethod
from typing import List, Optional

from bank_api.ports.repository_interface import RepositoryInterface
from bank_api.schemas.payment_account_schemas import (GetStatementDBOutput,
                                                      GetStatementFilters)
from bank_api.schemas.transfer_schemas import CreateTransferDBOutput
from config.database.models import PaymentAccount
from config.database.models.transaction import TransactionDetailType


class PaymentAccountRepositoryInterface(RepositoryInterface, ABC):
    @abstractmethod
    async def create(self, account: PaymentAccount) -> PaymentAccount:
        raise NotImplementedError

    @abstractmethod
    async def find(self, **kwargs) -> Optional[PaymentAccount]:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> List[PaymentAccount]:
        raise NotImplementedError

    @abstractmethod
    async def transfer(self, sender: PaymentAccount, receiver: PaymentAccount, amount: int, detail_type: TransactionDetailType) -> CreateTransferDBOutput:
        raise NotImplementedError

    @abstractmethod
    async def statement(self, account_id: str, filters: GetStatementFilters) -> GetStatementDBOutput:
        raise NotImplementedError
