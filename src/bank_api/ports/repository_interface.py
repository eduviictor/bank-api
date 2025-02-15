from abc import ABC
from collections.abc import Callable
from contextlib import _AsyncGeneratorContextManager
from typing import NewType

from sqlalchemy.ext.asyncio import AsyncSession

DBSession = NewType('DBSession', _AsyncGeneratorContextManager[AsyncSession])
ContextDBSession = Callable[[], DBSession]


class RepositoryInterface(ABC):
    def __init__(self, context_db_session: ContextDBSession):
        self.context_db_session = context_db_session
