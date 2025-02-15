import asyncio

from sqlalchemy import select

from bank_api.utils.password import hash_password
from config.database import async_session
from config.database.models import PaymentAccount, User
from config.database.models.payment_account import (PaymentAccountStatusEnum,
                                                    PaymentAccountType)


async def create_user_seed_data():
    async with async_session() as session:
        try:
            result = await session.execute(select(User))
            if result.scalars().first():
                print(
                    'The user table already contains data. Seed will not be executed.'
                )
                return

            user = User(username='admin', password=hash_password('admin'))
            session.add(user)
            await session.commit()

            print('User seed executed successfully!')
        except Exception as e:
            await session.rollback()
            print(f"Error executing user seed: {e}")
        finally:
            await session.close()


async def create_payment_account_seed_data():
    async with async_session() as session:
        try:
            result = await session.execute(select(PaymentAccount))
            if result.scalars().first():
                print(
                    'The payment account table already contains data. Seed will not be executed.'
                )
                return

            payments_accounts = [
                PaymentAccount(
                    status=PaymentAccountStatusEnum.OPEN,
                    name='Checking Account 1',
                    institution_code='001',
                    branch_code='0001',
                    account_code='123456',
                    account_type=PaymentAccountType.CHECKING,
                    tax_id='123456789',
                    balance=100000,
                ),
                PaymentAccount(
                    status=PaymentAccountStatusEnum.OPEN,
                    name='Savings Account 1',
                    institution_code='001',
                    branch_code='0001',
                    account_code='654321',
                    account_type=PaymentAccountType.SAVINGS,
                    tax_id='123456789',
                    balance=1,
                ),
                PaymentAccount(
                    status=PaymentAccountStatusEnum.OPEN,
                    name='Checking Account 2',
                    institution_code='001',
                    branch_code='0001',
                    account_code='654321',
                    account_type=PaymentAccountType.CHECKING,
                    tax_id='987654321',
                ),
            ]

            session.add_all(payments_accounts)
            await session.commit()

            print('Payment account seed executed successfully!')
        except Exception as e:
            await session.rollback()
            print(f"Error executing payment account seed: {e}")
        finally:
            await session.close()


async def main():
    await create_user_seed_data()
    await create_payment_account_seed_data()


if __name__ == '__main__':
    asyncio.run(main())
