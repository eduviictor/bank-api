# pylint: disable=too-many-lines

from unittest.mock import AsyncMock
from uuid import uuid4

from pytest import fixture, raises

from bank_api.exceptions.http_exceptions import HttpException
from bank_api.schemas.payment_account_schemas import (GetBalanceOutput,
                                                      GetStatementDBOutput,
                                                      StatementItem)
from bank_api.services.payment_account_service import PaymentAccountService
from config.database.models.payment_account import (PaymentAccount,
                                                    PaymentAccountStatusEnum,
                                                    PaymentAccountType)
from config.database.models.transaction import (Transaction,
                                                TransactionDetailType,
                                                TransactionStatus,
                                                TransactionType)


class TestPaymentAccountService:
    @fixture(autouse=True)
    def setup(self):
        self.payment_account_repository = AsyncMock()

        self.service = PaymentAccountService(
            payment_account_repository=self.payment_account_repository
        )

    @fixture(name='payment_account')
    def payment_account(self):
        return PaymentAccount(
            id=uuid4().hex,
            balance=0,
            status=PaymentAccountStatusEnum.OPEN,
            name='Test Account',
            institution_code='001',
            branch_code='0001',
            account_code='123456',
            account_type=PaymentAccountType.CHECKING,
            tax_id='12345678900',
            created_at='2021-01-01',
            updated_at='2021-01-01',
        )

    @fixture(name='transaction')
    def transaction(self):
        return Transaction(
            id=uuid4().hex,
            amount=100,
            balance_after=100,
            type=TransactionType.DEBIT,
            status=TransactionStatus.SUCCESS,
            detail_type=TransactionDetailType.WITHDRAW_TRANSFER,
            created_at='2021-01-01',
            updated_at='2021-01-01',
        )

    async def test_get_balance_raises_not_found_if_account_not_found(self):
        self.payment_account_repository.find.return_value = None

        with raises(HttpException) as exc:
            await self.service.get_balance(payment_account_id='123')

        assert exc.value.code == 404
        assert exc.value.message == 'Account not found'

    async def test_get_balance_returns_balance(self, payment_account):
        payment_account.balance = 100
        self.payment_account_repository.find.return_value = payment_account

        result = await self.service.get_balance(payment_account_id=payment_account.id)

        assert result == GetBalanceOutput(balance=payment_account.balance)

    async def test_statement_raises_not_found_if_account_not_found(self):
        self.payment_account_repository.find.return_value = None

        with raises(HttpException) as exc:
            await self.service.statement(payment_account_id='123', filters={})

        assert exc.value.code == 404
        assert exc.value.message == 'Account not found'

    async def test_statement_returns_statement(self, payment_account, transaction):
        self.payment_account_repository.find.return_value = payment_account
        statement_result = GetStatementDBOutput(
            total_items=1,
            total_pages=1,
            transactions=[
                StatementItem(
                    id=transaction.id,
                    amount=transaction.amount,
                    balance_after=transaction.balance_after,
                    status=transaction.status,
                    detail_type=transaction.detail_type,
                )
            ],
        )
        self.payment_account_repository.statement.return_value = statement_result

        filters = {
            'start_date': 1609459200,
            'end_date': 1609631999
        }
        result = await self.service.statement(payment_account_id=payment_account.id, filters=filters)

        assert result == statement_result

        self.payment_account_repository.statement.assert_called_once_with(
            payment_account.id, filters
        )
