import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.common.adapters.postgres.singleton_async_pool import (
    SingletonAsyncPool,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def setup_async_pool(_app: FastAPI) -> AsyncIterator[None]:
    pool = SingletonAsyncPool.get_instance()
    await pool.open()
    logger.info("Async Connection Pool started...")
    yield

    await pool.close()


lifespans = [setup_async_pool]
