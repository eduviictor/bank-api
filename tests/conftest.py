# pylint: disable=R0801
import os
import traceback
from collections.abc import Callable
from contextlib import asynccontextmanager

import pytest
from asgi_lifespan import LifespanManager
from dotenv import load_dotenv
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import settings
from bank_api.utils.log import logger
from config.database.models import ORMBaseModel
from main import create_app

pytest_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pytest.env')
load_dotenv(pytest_env_path, override=True)
logger.info(f"DATABASE_URL={os.getenv('DATABASE_URL')}")


async def load_server(create_app: Callable[[], FastAPI]):
    try:
        app = create_app()
        """Async server client that handles lifespan and teardown"""
        async with LifespanManager(app):
            yield app
    except Exception:
        traceback.print_exc()
    finally:
        # await clear_database(app)
        pass


@pytest.fixture(scope='session')
async def create_database_if_not_exists():
    try:
        engine = create_async_engine(settings.DATABASE_URL)
        async with engine.begin() as conn:
            print('Database already exists')
    except Exception:
        print('Database does not exist, creating...')
        url_without_db = settings.DATABASE_URL.replace('test_db', '')
        engine = create_async_engine(url_without_db)
        conn = await engine.connect()
        await conn.execution_options(isolation_level='AUTOCOMMIT')
        await conn.execute(text('CREATE DATABASE test_db;'))
    finally:
        await engine.dispose()


@pytest.fixture
async def get_db():
    """
    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.
    """
    logger.info(f'settings.DATABASE_URL: {settings.DATABASE_URL}')
    engine = create_async_engine(settings.DATABASE_URL)
    conn = None

    try:
        conn = await engine.connect()
        await conn.execution_options(isolation_level='AUTOCOMMIT')
        await conn.run_sync(ORMBaseModel.metadata.drop_all)
        await conn.run_sync(ORMBaseModel.metadata.create_all)
        _session = sessionmaker(conn, expire_on_commit=False, class_=AsyncSession)  # type: ignore

        @asynccontextmanager
        async def _get_db():
            session: AsyncSession
            async with _session() as session:  # type: ignore
                try:
                    yield session
                    await session.commit()
                except Exception as exc:
                    await session.rollback()
                    raise exc
                finally:
                    await session.close()

        yield _get_db

    except Exception as e:
        logger.warning(str(e))

    finally:
        if conn:
            await conn.close()
        await engine.dispose()


@pytest.fixture()
async def transaction(_engine):
    conn = await _engine.begin()
    try:
        yield conn
    finally:
        await conn.rollback()


@pytest.fixture(scope='function', autouse=True)
async def server():
    async for _server in load_server(create_app):
        yield _server


@pytest.fixture(scope='function')
async def client(server):  # pylint: disable=redefined-outer-name
    async with AsyncClient(transport=ASGITransport(app=server), base_url='http://test') as _client:
        yield _client
