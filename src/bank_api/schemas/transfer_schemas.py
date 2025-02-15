from enum import StrEnum

from pydantic import BaseModel, Field


class CreateTransferInput(BaseModel):
    amount: float = Field(..., gt=0, description='Amount to be transferred in decimal format', example=100)
    sender_account_id: str = Field(..., pattern=r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    receiver_account_id: str = Field(..., pattern=r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')


class MoveInternalFoundsType(StrEnum):
    INVESTMENT = 'investment'
    WITHDRAW = 'withdraw'


class MoveInternalFoundsInput(BaseModel):
    amount: float = Field(..., gt=0, description='Amount to be transferred in decimal format', example=100)
    account_id: str = Field(..., pattern=r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    type: MoveInternalFoundsType = Field(..., description='Type of the movement', example=MoveInternalFoundsType.INVESTMENT)
