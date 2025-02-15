from traceback import format_exc

from sqlalchemy import and_, select

from bank_api.exceptions.user_exceptions import UserException
from bank_api.ports.user_repository_interface import UserRepositoryInterface
from bank_api.utils.log import logger
from config.database.models.user import User


class UserRepository(UserRepositoryInterface):
    async def create(self, instance: User):
        try:
            async with self.context_db_session() as session:
                session.add(instance)
                await session.commit()
                return instance
        except Exception:
            logger.error(f'[UserRepository.create] cant create => {str(format_exc())}')
            return None

    async def find_by_id(self, **kwargs) -> User | None:
        conditions = []
        for key, value in kwargs.items():
            conditions.append(getattr(User, key) == value)

        try:
            async with self.context_db_session() as session:
                query = select(User).where(and_(*conditions))

                result = await session.execute(query)
                return result.scalar_one_or_none()
        except Exception as exc:
            logger.error(f'[UserRepository] error get by {kwargs} => {str(exc)}')
            return None

    async def find_all(self, **kwargs):
        conditions = []
        for key, value in kwargs.items():
            conditions.append(getattr(User, key) == value)

        try:
            async with self.context_db_session() as session:
                query = select(User).where(and_(*conditions))

                result = await session.execute(query)
                return result.scalars().all()
        except Exception as exc:
            logger.error(f'[UserRepository] error list by {kwargs} => {str(exc)}')
            raise UserException(message=str(exc)) from exc

    async def get_by_username(self, username):
        try:
            async with self.context_db_session() as session:
                query = select(User).where(User.username == username)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except Exception as exc:
            logger.error(f'[UserRepository] error get by username {username} => {str(exc)}')
            return None
