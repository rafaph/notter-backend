from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_lifespan_manager import LifespanManager

from src.common.adapters.postgres.singleton_async_pool import (
    SingletonAsyncPool,
)


@asynccontextmanager
async def setup_async_pool(_app: FastAPI) -> AsyncIterator[None]:
    pool = SingletonAsyncPool.get_instance()
    await pool.open()

    yield

    await pool.close()


lifespan = LifespanManager(
    [
        setup_async_pool,
    ],
)
