from psycopg import AsyncConnection
from psycopg.rows import DictRow, dict_row
from psycopg_pool import AsyncConnectionPool

from src.common.settings import settings


class SingletonAsyncPool:
    _instance: AsyncConnectionPool[AsyncConnection[DictRow]] | None = None

    @classmethod
    def get_instance(
        cls,
    ) -> AsyncConnectionPool[AsyncConnection[DictRow]]:
        if cls._instance is None:
            cls._instance = AsyncConnectionPool(
                str(settings.DATABASE_URL),
                open=False,
                kwargs={
                    "row_factory": dict_row,
                },
            )

        return cls._instance
