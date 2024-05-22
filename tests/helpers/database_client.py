from psycopg import AsyncConnection, AsyncCursor
from psycopg.abc import Params, Query
from psycopg.rows import DictRow
from psycopg_pool import AsyncConnectionPool


class DatabaseClient:
    def __init__(
        self, pool: AsyncConnectionPool[AsyncConnection[DictRow]]
    ) -> None:
        self._pool = pool

    async def query(
        self,
        query: Query,
        params: Params | None = None,
    ) -> AsyncCursor[DictRow]:
        async with self._pool.connection() as connection:
            return await connection.execute(query, params)
