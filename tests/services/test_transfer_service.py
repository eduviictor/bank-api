# pylint: disable=too-many-lines

from unittest.mock import AsyncMock
from uuid import uuid4

from pytest import fixture, raises

from bank_api.exceptions.http_exceptions import HttpException
from bank_api.exceptions.payment_account_exceptions import \
    PaymentAccountException
from bank_api.schemas.transfer_schemas import (CreateTransferDBOutput,
                                               CreateTransferInput,
                                               MoveInternalFoundsInput,
                                               MoveInternalFoundsType)
from bank_api.services.transfer_service import TransferService
from config.database.models.payment_account import (PaymentAccount,
                                                    PaymentAccountStatusEnum,
                                                    PaymentAccountType)
from config.database.models.transaction import (Transaction,
                                                TransactionDetailType,
                                                TransactionStatus,
                                                TransactionType)


class TestTransferService:
    @fixture(autouse=True)
    def setup(self):
        self.payment_account_repository = AsyncMock()

        self.service = TransferService(
            payment_account_repository=self.payment_account_repository,
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

    @fixture(name='transfer_params')
    def transfer_params(self, payment_account):
        return CreateTransferInput(
            amount=1,
            sender_account_id=str(uuid4()),
            receiver_account_id=str(uuid4()),
        )

    @fixture(name='move_params')
    def move_internal_founds_params(self, payment_account):
        return MoveInternalFoundsInput(
            amount=1,
            account_id=str(uuid4()),
            type=MoveInternalFoundsType.INVESTMENT,
        )

    async def test_transfer_raises_not_found_if_sender_account_not_found(self, payment_account, transfer_params):
        self.payment_account_repository.find.return_value = None

        with raises(HttpException) as exc:
            await self.service.transfer(transfer_params)

        assert exc.value.code == 404

    async def test_transfer_raises_not_found_if_receiver_account_not_found(self, payment_account, transfer_params):
        self.payment_account_repository.find.side_effect = [payment_account, None]

        with raises(HttpException) as exc:
            await self.service.transfer(transfer_params)

        assert exc.value.code == 404

    async def test_transfer_raises_bad_request_if_sender_and_receiver_accounts_are_the_same(self, payment_account, transfer_params):
        self.payment_account_repository.find.side_effect = [payment_account, payment_account]

        with raises(HttpException) as exc:
            await self.service.transfer(transfer_params)

        assert exc.value.code == 400

    async def test_transfer_raises_bad_request_if_insufficient_funds(self, payment_account, transfer_params):
        self.payment_account_repository.find.side_effect = [payment_account, payment_account]

        with raises(HttpException) as exc:
            await self.service.transfer(transfer_params)

        assert exc.value.code == 400

    async def test_transfer_raises_bad_request_if_transfer_fails(self, payment_account, transfer_params):
        self.payment_account_repository.find.side_effect = [payment_account, payment_account]
        self.payment_account_repository.transfer.side_effect = PaymentAccountException('Error')

        with raises(HttpException) as exc:
            await self.service.transfer(transfer_params)

        assert exc.value.code == 400

    async def test_transfer_returns_ok_after_transfer(self, payment_account, transfer_params):
        sender_account = PaymentAccount(
            id=str(uuid4()),
            balance=100,
            status=PaymentAccountStatusEnum.OPEN,
            name='Sender Account',
            institution_code='001',
            branch_code='0001',
            account_code='654321',
            account_type=PaymentAccountType.CHECKING,
            tax_id='98765432100',
            created_at='2021-01-01',
            updated_at='2021-01-01',
        )
        self.payment_account_repository.find.side_effect = [sender_account, payment_account]
        transfer_db_output = CreateTransferDBOutput(
            credit_transaction_id=str(uuid4()),
            debit_transaction_id=str(uuid4()),
        )
        self.payment_account_repository.transfer.return_value = transfer_db_output

        result = await self.service.transfer(transfer_params)

        assert result.balance == sender_account.balance
        assert result.transaction_id == transfer_db_output.debit_transaction_id


    async def test_move_internal_founds_raises_not_found_if_account_not_found(self, payment_account, move_params):
        self.payment_account_repository.find.return_value = None

        with raises(HttpException) as exc:
            await self.service.move_internal_founds(move_params)

        assert exc.value.code == 404

    async def test_move_internal_founds_raises_bad_request_if_insufficient_funds(self, payment_account, move_params):
        self.payment_account_repository.find.return_value = payment_account

        with raises(HttpException) as exc:
            await self.service.move_internal_founds(move_params)

        assert exc.value.code == 400

    async def test_move_internal_founds_raises_bad_request_if_receiver_account_not_found(self, payment_account, move_params):
        payment_account.balance = 100
        move_params.type = MoveInternalFoundsType.WITHDRAW
        self.payment_account_repository.find.side_effect = [payment_account, None]

        with raises(HttpException) as exc:
            await self.service.move_internal_founds(move_params)

        assert exc.value.code == 404

    async def test_move_internal_founds_returns_ok_after_transfer(self, payment_account, move_params):
        payment_account.balance = 100
        account_receiver = PaymentAccount(
            id=str(uuid4()),
            balance=100,
            status=PaymentAccountStatusEnum.OPEN,
            name='Receiver Account',
            institution_code='001',
            branch_code='0001',
            account_code='654321',
            account_type=PaymentAccountType.SAVINGS,
            tax_id='98765432100',
            created_at='2021-01-01',
            updated_at='2021-01-01',
        )
        move_params.type = MoveInternalFoundsType.WITHDRAW
        self.payment_account_repository.find.side_effect = [payment_account, account_receiver]
        transfer_db_output = CreateTransferDBOutput(
            credit_transaction_id=str(uuid4()),
            debit_transaction_id=str(uuid4()),
        )
        self.payment_account_repository.transfer.return_value = transfer_db_output

        result = await self.service.move_internal_founds(move_params)

        assert result.checking_balance == payment_account.balance
        assert result.savings_balance == account_receiver.balance
