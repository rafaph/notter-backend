import asyncio
import os
from pathlib import Path
from types import TracebackType

from faker import Faker
from psycopg import AsyncConnection
from psycopg.rows import DictRow, dict_row
from psycopg_pool import AsyncConnectionPool


class DatabaseTest:
    _faker = Faker("en_US")

    def __init__(self) -> None:
        self._database_name = "".join(self._faker.random_letters(60)).lower()
        self._base_connection_str = "postgres://admin:admin@postgres:5432"
        self.pool: AsyncConnectionPool[AsyncConnection[DictRow]] | None = None

    async def up(self) -> None:
        await self._create_database()
        try:
            await self._migrate()
            self.pool = AsyncConnectionPool(
                self.database_url,
                open=False,
                kwargs={
                    "row_factory": dict_row,
                },
            )
            await self.pool.open(wait=True)
        except Exception as error:
            await self._drop_database()
            raise error

    async def down(self) -> None:
        if self.pool is not None:
            await self.pool.close()

        await self._drop_database()

    @property
    def database_url(self) -> str:
        return f"{self._base_connection_str}/{self._database_name}"

    async def _query(self, query: str) -> None:
        async with await AsyncConnection.connect(
            f"{self._base_connection_str}/postgres",
            autocommit=True,
        ) as connection:
            await connection.execute(query)

    async def _create_database(self) -> None:
        query = f"CREATE DATABASE {self._database_name} WITH OWNER = admin;"
        await self._query(query)

    async def _drop_database(self) -> None:
        query = f"DROP DATABASE IF EXISTS {self._database_name};"
        await self._query(query)

    async def _migrate(self) -> None:
        cmd = [
            "goose",
            "-dir",
            "migrations",
            "postgres",
            self.database_url,
            "up",
        ]
        env = {**os.environ}
        cwd = Path(__file__).resolve().parent.parent.parent
        process = await asyncio.create_subprocess_shell(
            " ".join(cmd),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
            cwd=cwd,
        )
        stdout, stderr = await process.communicate()
        if process.returncode:
            output = "" if stdout is None else stdout.decode("utf-8")
            error = "" if stderr is None else stderr.decode("utf-8")
            msg = f"Failed to migrate:\nstdout: {output}\nstderr: {error}"
            raise Exception(msg)

    async def __aenter__(
        self,
    ) -> AsyncConnectionPool[AsyncConnection[DictRow]]:
        await self.up()

        assert self.pool, "Pool should not be None, forgot to call up()?"

        return self.pool

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.down()
