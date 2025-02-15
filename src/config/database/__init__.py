from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from bank_api.utils.enviroment import EnvironmentSet
from config.database.models import ORMBaseModel
from settings import DATABASE_URL, ENVIRONMENT

engine = create_async_engine(
    DATABASE_URL, pool_pre_ping=False, pool_recycle=3600, echo_pool=False
)
async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


@asynccontextmanager
async def get_db():
    session: AsyncSession
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as exc:
            await session.rollback()
            raise exc
        finally:
            await session.close()


async def create_db():
    if ENVIRONMENT == EnvironmentSet.DEVELOPMENT:
        async with engine.begin() as conn:
            await conn.run_sync(ORMBaseModel.metadata.create_all)


async def drop_db():
    if ENVIRONMENT == EnvironmentSet.DEVELOPMENT:
        async with engine.begin() as conn:
            await conn.run_sync(ORMBaseModel.metadata.drop_all)
