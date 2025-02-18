from uuid import uuid4

from pytest import fixture, mark

from bank_api.adapters.repositories.payment_account_repository import \
    PaymentAccountRepository
from bank_api.schemas.payment_account_schemas import GetStatementFilters
from config.database.models.payment_account import (PaymentAccount,
                                                    PaymentAccountType)
from config.database.models.transaction import TransactionDetailType


class TestPaymentAccountRepository:
    @fixture(autouse=True)
    async def setup(self, get_db):
        self.payment_account_repository = PaymentAccountRepository(context_db_session=get_db)

    @fixture
    async def payment_account_instance_checking(self):
        async with self.payment_account_repository.context_db_session() as session:
            instance = PaymentAccount(
                balance=1000,
                name='test',
                institution_code='123',
                branch_code='123',
                account_code='123',
                account_type=PaymentAccountType.CHECKING,
                tax_id='123456789',
            )
            session.add(instance)
            await session.commit()
            return instance

    @fixture
    async def payment_account_instance_savings(self):
        async with self.payment_account_repository.context_db_session() as session:
            instance = PaymentAccount(
                balance=100,
                name='test',
                institution_code='123',
                branch_code='123',
                account_code='123',
                account_type=PaymentAccountType.SAVINGS,
                tax_id='987654321',
            )
            session.add(instance)
            await session.commit()
            return instance

    @mark.asyncio
    async def test_create_with_error(self):
        result = await self.payment_account_repository.create(PaymentAccount())
        assert result is None

    @mark.asyncio
    async def test_create_with_success(self):
        result = await self.payment_account_repository.create(
            PaymentAccount(
                balance=100000,
                name='test',
                institution_code='123',
                branch_code='123',
                account_code='123',
                account_type=PaymentAccountType.CHECKING,
                tax_id='123456789',
            )
        )
        assert result
        assert isinstance(result, PaymentAccount)

    @mark.asyncio
    async def test_find_with_not_found(self):
        result = await self.payment_account_repository.find(id=str(uuid4()))
        assert result is None

    @mark.asyncio
    async def test_find_with_success(self, payment_account_instance_checking):
        result = await self.payment_account_repository.find(id=payment_account_instance_checking.id)
        assert result
        assert isinstance(result, PaymentAccount)

    @mark.asyncio
    async def test_find_all_return_empty_list(self):
        result = await self.payment_account_repository.find_all(id=str(uuid4()))
        assert result == []

    @mark.asyncio
    async def test_find_all_with_success(self, payment_account_instance_checking):
        result = await self.payment_account_repository.find_all()
        assert result
        assert isinstance(result, list)
        assert payment_account_instance_checking.id == result[0].id

    @mark.asyncio
    async def test_statement_with_empty_transactions(self):
        result = await self.payment_account_repository.statement(
            account_id=str(uuid4()),
            filters=GetStatementFilters(
                start=1672531200,
                end=1704067200
            )
        )
        assert result.transactions == []

    @mark.asyncio
    async def test_transfer_success(self, payment_account_instance_checking, payment_account_instance_savings):
        amount = 50
        detail_type = TransactionDetailType.TRANSFER

        balance_before_sender = payment_account_instance_checking.balance
        balance_before_receiver = payment_account_instance_savings.balance

        result = await self.payment_account_repository.transfer(
            sender=payment_account_instance_checking,
            receiver=payment_account_instance_savings,
            amount=amount,
            detail_type=detail_type
        )

        assert result
        assert result.credit_transaction_id
        assert result.debit_transaction_id

        sender_account = await self.payment_account_repository.find(id=payment_account_instance_checking.id)
        receiver_account = await self.payment_account_repository.find(id=payment_account_instance_savings.id)

        assert sender_account.balance == balance_before_sender - amount
        assert receiver_account.balance == balance_before_receiver + amount
