from abc import ABC, abstractmethod

from bank_api.ports.payment_account_repository_interface import \
    PaymentAccountRepositoryInterface
from bank_api.schemas.transfer_schemas import (CreateTransferOutput,
                                               MoveInternalFoundsInput,
                                               MoveInternalFoundsOutput)


class TransferServiceInterface(ABC):
    def __init__(
        self,
        payment_account_repository: PaymentAccountRepositoryInterface,
    ):
        self.payment_account_repository = payment_account_repository

    @abstractmethod
    async def transfer(self, sender_id: str, receiver_id: str, amount: int) -> CreateTransferOutput:
        raise NotImplementedError

    @abstractmethod
    async def move_internal_founds(
        self, params: MoveInternalFoundsInput
    ) -> MoveInternalFoundsOutput:
        raise NotImplementedError
