from pydantic import BaseModel, Field


class CreateTransferInput(BaseModel):
    amount: float = Field(..., gt=0, description='Amount to be transferred in decimal format', example=100)
    sender_account_id: str = Field(..., pattern=r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
    receiver_account_id: str = Field(..., pattern=r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
