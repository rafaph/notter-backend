import os
from collections.abc import AsyncIterator

import pytest
from psycopg import AsyncConnection
from psycopg.rows import DictRow
from psycopg_pool import AsyncConnectionPool

from tests.helpers.database_test import DatabaseTest

os.environ["LOG_LEVEL"] = "ERROR"


@pytest.fixture()
def anyio_backend() -> tuple[str, dict[str, bool]]:
    return ("asyncio", {"use_uvloop": True})


@pytest.fixture()
async def pool() -> (
    AsyncIterator[AsyncConnectionPool[AsyncConnection[DictRow]]]
):
    async with DatabaseTest() as pool:
        yield pool


@pytest.fixture()
async def connection(
    pool: AsyncConnectionPool[AsyncConnection[DictRow]],
) -> AsyncIterator[AsyncConnection[DictRow]]:
    async with pool.connection() as connection:
        yield connection
