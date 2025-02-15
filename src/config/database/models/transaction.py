from enum import StrEnum

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from .base import ORMBaseModel


class TransactionType(StrEnum):
    DEBIT = 'debit'
    CREDIT = 'credit'


class TransactionStatus(StrEnum):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'


class TransactionDetailType(StrEnum):
    WITHDRAW_TRANSFER = 'withdraw_transfer'
    INVESTMENT = 'investment_transfer'
    TRANSFER = 'transfer'


class Transaction(ORMBaseModel):
    __tablename__ = 'transaction'  # type: ignore[assignment]

    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    balance_after: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(
        Enum(TransactionType, name='transaction_type_enum'), nullable=False
    )
    status: Mapped[str] = mapped_column(
        Enum(TransactionStatus, name='transaction_status_enum'),
        default=TransactionStatus.PENDING,
    )
    detail_type: Mapped[str] = mapped_column(
        Enum(TransactionDetailType, name='transaction_detail_type_enum'), nullable=False
    )
    payment_account_id: Mapped[int] = mapped_column(
        ForeignKey('payment_account.id'), nullable=False
    )
    parent_transaction_id: Mapped[str] = mapped_column(
        ForeignKey('transaction.id'), nullable=True
    )

    payment_account: Mapped['PaymentAccount'] = relationship(  # noqa
        'PaymentAccount', backref=None
    )
    parent_transaction: Mapped['Transaction'] = relationship(
        'Transaction', remote_side='Transaction.id', backref=None
    )

    __table_args__ = (
        CheckConstraint('amount >= 0', name='check_amount_non_negative'),
        CheckConstraint('balance_after >= 0', name='check_balance_after_non_negative'),
    )

    @validates('amount')
    def validate_balance(self, key, value):
        if value < 0:
            raise ValueError('Amount must be greater than or equal to 0')
        return value

    @validates('balance_after')
    def validate_balance_after(self, key, value):
        if value < 0:
            raise ValueError('Balance after must be greater than or equal to 0')
        return value
