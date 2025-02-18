
from datetime import datetime
from traceback import format_exc

from sqlalchemy import DateTime, and_, cast, func, select

from bank_api.exceptions.payment_account_exceptions import \
    PaymentAccountException
from bank_api.ports.payment_account_repository_interface import \
    PaymentAccountRepositoryInterface
from bank_api.schemas.payment_account_schemas import (GetStatementDBOutput,
                                                      GetStatementFilters,
                                                      StatementItem)
from bank_api.schemas.transfer_schemas import CreateTransferDBOutput
from bank_api.utils.log import logger
from config.database.models.payment_account import PaymentAccount
from config.database.models.transaction import (Transaction,
                                                TransactionDetailType,
                                                TransactionStatus,
                                                TransactionType)


class PaymentAccountRepository(PaymentAccountRepositoryInterface):
    async def create(self, instance: PaymentAccount):
        try:
            async with self.context_db_session() as session:
                session.add(instance)
                await session.commit()
                return instance
        except Exception:
            logger.error(f'[PaymentAccountRepository.create] cant create => {str(format_exc())}')
            return None

    async def find(self, **kwargs):
        try:
            async with self.context_db_session() as session:
                query = select(PaymentAccount).where(and_(*[getattr(PaymentAccount, key) == value for key, value in kwargs.items()]))
                result = await session.execute(query)
                return result.scalars().first()
        except Exception as exc:
            logger.error(f'[PaymentAccountRepository] error find by {kwargs} => {str(exc)}')
            raise PaymentAccountException(message=str(exc)) from exc

    async def find_all(self, **kwargs):
        conditions = []
        for key, value in kwargs.items():
            conditions.append(getattr(PaymentAccount, key) == value)

        try:
            async with self.context_db_session() as session:
                query = select(PaymentAccount).where(and_(*conditions))

                result = await session.execute(query)
                return result.scalars().all()
        except Exception as exc:
            logger.error(f'[PaymentAccountRepository] error list by {kwargs} => {str(exc)}')
            raise PaymentAccountException(message=str(exc)) from exc

    async def transfer(self, sender: PaymentAccount, receiver: PaymentAccount, amount: int, detail_type: TransactionDetailType) -> CreateTransferDBOutput:
        try:
            async with self.context_db_session() as session:
                async with session.begin():
                    sender.balance -= amount
                    receiver.balance += amount

                    transaction_debt = self.__build_transaction(
                        amount=amount,
                        balance_after=sender.balance,
                        type=TransactionType.DEBIT,
                        status=TransactionStatus.PENDING,
                        detail_type=detail_type,
                        payment_account_id=sender.id
                    )

                    session.add(transaction_debt)
                    await session.flush()

                    transaction_credit = self.__build_transaction(
                        amount=amount,
                        balance_after=receiver.balance,
                        type=TransactionType.CREDIT,
                        status=TransactionStatus.PENDING,
                        detail_type=detail_type,
                        payment_account_id=receiver.id,
                        parent_transaction_id=transaction_debt.id
                    )


                    session.add_all([sender, receiver, transaction_credit])
                    await session.commit()
                    return CreateTransferDBOutput(
                        credit_transaction_id=str(transaction_credit.id),
                        debit_transaction_id=str(transaction_debt.id)
                    )
        except Exception as exc:
            logger.error(f'[PaymentAccountRepository.transfer] error during transfer => {str(exc)}')
            raise PaymentAccountException(message=str(exc)) from exc

    def __build_transaction(
        self,
        amount: int,
        balance_after: int,
        type: str,
        status: str,
        payment_account_id: int,
        detail_type: TransactionDetailType,
        parent_transaction_id: int | None = None
    ) -> Transaction:
        return Transaction(
            amount=amount,
            balance_after=balance_after,
            type=type,
            status=status,
            payment_account_id=payment_account_id,
            detail_type=detail_type,
            parent_transaction_id=parent_transaction_id
        )

    async def statement(self, account_id: str, filters: GetStatementFilters) -> GetStatementDBOutput:
        try:
            async with self.context_db_session() as session:
                conditions = [Transaction.payment_account_id == account_id]

                if filters.start:
                    conditions.append(Transaction.created_at >= cast(datetime.fromtimestamp(filters.start), DateTime))
                if filters.end:
                    conditions.append(Transaction.created_at <= cast(datetime.fromtimestamp(filters.end), DateTime))

                query = select(Transaction).where(and_(*conditions))

                total_items_query = select(func.count()).select_from(query.subquery())
                total_items_result = await session.execute(total_items_query)
                total_items = total_items_result.scalar()

                if filters.page and filters.limit:
                    offset = (filters.page - 1) * filters.limit
                    query = query.limit(filters.limit).offset(offset)

                result = await session.execute(query)
                transactions = result.scalars().all()

                total_pages = (total_items + filters.limit - 1) // filters.limit if filters.limit else 1

                return GetStatementDBOutput(
                    transactions=[
                        StatementItem(
                            id=str(transaction.id),
                            amount=transaction.amount,
                            balance_after=transaction.balance_after,
                            detail_type=transaction.detail_type.value,
                            status=transaction.status.value
                        )
                        for transaction in transactions
                    ],
                    total_items=total_items,
                    total_pages=total_pages
                )
        except Exception as exc:
            logger.error(f'[PaymentAccountRepository.statement] error during statement => {str(exc)}')
            raise PaymentAccountException(message=str(exc)) from exc
