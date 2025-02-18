from enum import StrEnum

from pydantic import BaseModel, Field


class CreateTransferInput(BaseModel):
    amount: float = Field(..., gt=0, description='Amount to be transferred in decimal format', example=100)
    sender_account_id: str = Field(..., pattern=r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    receiver_account_id: str = Field(..., pattern=r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')


class CreateTransferOutput(BaseModel):
    balance: float = Field(..., description='Balance after the transfer', example=100)
    transaction_id: str = Field(..., description='Transaction ID', example='123e4567-e89b-12d3-a456-426614174000')

class MoveInternalFoundsType(StrEnum):
    INVESTMENT = 'investment'
    WITHDRAW = 'withdraw'


class MoveInternalFoundsInput(BaseModel):
    amount: float = Field(..., gt=0, description='Amount to be transferred in decimal format', example=100)
    account_id: str = Field(..., pattern=r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    type: MoveInternalFoundsType = Field(..., description='Type of the movement', example=MoveInternalFoundsType.INVESTMENT)

class MoveInternalFoundsOutput(BaseModel):
    checking_balance: float = Field(..., description='Checking account balance after the transfer', example=100)
    savings_balance: float = Field(..., description='Savings account balance after the transfer', example=100)


class CreateTransferDBOutput(BaseModel):
    credit_transaction_id: str = Field(..., description='Credit transaction ID', example='123e4567-e89b-12d3-a456-426614174000')
    debit_transaction_id: str = Field(..., description='Debit transaction ID', example='123e4567-e89b-12d3-a456-426614174000')
