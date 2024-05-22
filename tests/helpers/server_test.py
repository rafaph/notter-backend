import asyncio
import os
import secrets
import signal
import socket
import subprocess
import time
from pathlib import Path
from types import TracebackType

import httpx
from fastapi import status
from psycopg import AsyncConnection
from psycopg.rows import DictRow
from psycopg_pool import AsyncConnectionPool

from tests.helpers.database_test import DatabaseTest


class ServerTest:
    def __init__(self, env: dict[str, str] | None = None) -> None:
        self._process: subprocess.Popen[bytes] | None = None
        self._database_test = DatabaseTest()
        self._http_client = httpx.AsyncClient()
        self._env = env or {}

    async def up(self) -> None:
        # up database
        await self._database_test.up()

        # up http server
        try:
            cwd = Path(__file__).resolve().parent.parent.parent
            port = self._get_free_port()
            env = {
                **os.environ,
                "DATABASE_URL": self._database_test.database_url,
                "SECRET_KEY": secrets.token_hex(64),
                "ALGORITHM": "HS512",
                "EXPIRATION_TIME_MINUTES": "10",
                **self._env,
                "TESTING": "true",
            }
            self._process = subprocess.Popen(
                [
                    ".venv/bin/fastapi",
                    "run",
                    "--no-reload",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    port,
                    "src/main.py",
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=env,
                cwd=cwd,
            )
            self._http_client.base_url = httpx.URL(f"http://127.0.0.1:{port}")
            await self._health_check()
        except Exception as error:
            await self.down()
            raise error

    async def down(self) -> None:
        self._kill_process()

        await self._http_client.aclose()

        await self._database_test.down()

    async def __aenter__(
        self,
    ) -> tuple[
        httpx.AsyncClient,
        AsyncConnectionPool[AsyncConnection[DictRow]],
    ]:
        await self.up()

        assert (
            self._database_test.pool
        ), "Pool should not be None, forgot to call up()?"

        return (self._http_client, self._database_test.pool)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.down()

    def _get_free_port(self, tries: int = 600, delay: float = 0.1) -> str:
        for _ in range(tries):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(("127.0.0.1", 0))
                    return str(s.getsockname()[1])
            except Exception:  # noqa: S110
                pass
            time.sleep(delay)

        msg = "Failed to get a free port"
        raise Exception(msg)

    async def _health_check(
        self, tries: int = 300, delay: float = 0.1
    ) -> None:
        for _ in range(tries):
            try:
                response = await self._http_client.get("/healthz")
                if response.status_code == status.HTTP_204_NO_CONTENT:
                    return
            except Exception:  # noqa: S110
                pass
            await asyncio.sleep(delay)

        msg = "Server is not healthy"
        raise Exception(msg)

    def _kill_process(self) -> None:
        if self._process is not None:
            self._process.send_signal(signal.SIGTERM)
            self._process.wait()
