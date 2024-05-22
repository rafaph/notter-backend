from psycopg import AsyncConnection
from psycopg.rows import DictRow
from psycopg_pool import AsyncConnectionPool

from src.common.adapters.postgres.singleton_async_pool import (
    SingletonAsyncPool,
)


def get_pool() -> AsyncConnectionPool[AsyncConnection[DictRow]]:
    return SingletonAsyncPool.get_instance()
