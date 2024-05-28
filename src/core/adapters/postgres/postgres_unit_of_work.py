from types import TracebackType
from typing import Self

from psycopg import AsyncConnection
from psycopg.rows import DictRow
from psycopg_pool import AsyncConnectionPool

from src.core.adapters.postgres.repositories import (
    PostgresCategoryRepository,
    PostgresNoteCategoryRepository,
    PostgresNoteRepository,
)
from src.core.ports.unit_of_work import UnitOfWork


class PostgresUnitOfWork(UnitOfWork):
    def __init__(
        self, pool: AsyncConnectionPool[AsyncConnection[DictRow]]
    ) -> None:
        self._pool = pool
        self._connection: AsyncConnection[DictRow] | None = None

    async def __aenter__(self) -> Self:
        self._connection = await self._pool.getconn()
        self.note_repository = PostgresNoteRepository(self._connection)
        self.category_repository = PostgresCategoryRepository(self._connection)
        self.note_category_repository = PostgresNoteCategoryRepository(
            self._connection,
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        if self._connection:
            await self._connection.close()
            await self._pool.putconn(self._connection)

    async def commit(self) -> None:
        if self._connection:
            await self._connection.commit()

    async def rollback(self) -> None:
        if self._connection:
            await self._connection.rollback()
