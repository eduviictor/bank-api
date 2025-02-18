from uuid import uuid4

from pytest import fixture, mark

from bank_api.adapters.repositories.user_repository import UserRepository
from config.database.models.user import User


class TestUserRepository:
    @fixture(autouse=True)
    async def setup(self, get_db):
        self.user_repository = UserRepository(context_db_session=get_db)

    @fixture
    async def user_instance(self):
        async with self.user_repository.context_db_session() as session:
            instance = User(
                username='test',
                password='test',
            )
            session.add(instance)
            await session.commit()
            return instance

    @mark.asyncio
    async def test_create_with_error(self):
        result = await self.user_repository.create(User())
        assert result is None

    @mark.asyncio
    async def test_create_with_success(self):
        result = await self.user_repository.create(
            User(
                username='test',
                password='test',
            )
        )
        assert result
        assert isinstance(result, User)

    @mark.asyncio
    async def test_find_by_id_with_error(self):
        result = await self.user_repository.find_by_id(id=str(uuid4()))
        assert result is None

    @mark.asyncio
    async def test_find_by_id_with_success(self, user_instance):
        result = await self.user_repository.find_by_id(id=user_instance.id)
        assert result is not None
        assert isinstance(result, User)

    @mark.asyncio
    async def test_find_all_with_error(self):
        result = await self.user_repository.find_all(id=str(uuid4()))
        assert result == []

    @mark.asyncio
    async def test_find_all_with_success(self, user_instance):
        result = await self.user_repository.find_all()
        assert result
        assert isinstance(result, list)
        assert user_instance.id == result[0].id

    @mark.asyncio
    async def test_get_by_username_with_error(self):
        result = await self.user_repository.get_by_username('test')
        assert result is None

    @mark.asyncio
    async def test_get_by_username_with_success(self, user_instance):
        result = await self.user_repository.get_by_username('test')
        assert result
        assert isinstance(result, User)
        assert result.id == user_instance.id
