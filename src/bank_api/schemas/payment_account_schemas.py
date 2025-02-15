from pydantic import BaseModel, Field


class GetBalanceOutput(BaseModel):
    balance: int

class GetStatementFilters(BaseModel):
    start: int | None = Field(None, description='Start date in timestamp format')
    end: int | None = Field(None, description='End date in timestamp format')
    page: int = Field(1, description='Page number')
    limit: int = Field(10, description='Number of items per page')

class StatementItem(BaseModel):
    id: str
    amount: int
    balance_after: int
    description: str
    status: str

class GetStatementDBOutput(BaseModel):
    transactions: list[StatementItem]
    total_items: int
    total_pages: int

class GetStatementOutput(BaseModel):
    items: list[StatementItem]
    total_items: int
    total_pages: int
