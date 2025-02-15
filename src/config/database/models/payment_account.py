from enum import StrEnum

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import ORMBaseModel


class PaymentAccountStatusEnum(StrEnum):
    OPEN = 'open'
    CLOSED = 'closed'
    BLOCKED = 'blocked'


class PaymentAccountType(StrEnum):
    CHECKING = 'checking'
    SAVINGS = 'savings'


class PaymentAccount(ORMBaseModel):
    __tablename__ = 'payment_account'  # type: ignore[assignment]

    balance: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(
        Enum(PaymentAccountStatusEnum, name='payment_account_status_enum'),
        default=PaymentAccountStatusEnum.OPEN,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    institution_code: Mapped[str] = mapped_column(String(255), nullable=False)
    branch_code: Mapped[str] = mapped_column(String(255), nullable=False)
    account_code: Mapped[str] = mapped_column(String(255), nullable=False)
    account_type: Mapped[str] = mapped_column(
        Enum(PaymentAccountType, name='payment_account_type_enum'), nullable=False
    )
    tax_id: Mapped[str] = mapped_column(String(255), nullable=False)
