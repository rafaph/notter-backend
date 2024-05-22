import os

from src.common.types import ExceptionHandlerEntry

if os.getenv("TESTING") == "true":  # pragma: no cover
    from pytest_cov.embed import cleanup_on_sigterm  # type: ignore

    cleanup_on_sigterm()

from fastapi import FastAPI
from fastapi_lifespan_manager import LifespanManager

from src.auth.drivers.rest.exception_handlers import (
    exception_handlers as auth_exception_handlers,
)
from src.auth.drivers.rest.router import router as auth_router
from src.common.drivers.rest.lifespans import lifespans as common_lifespans
from src.common.drivers.rest.router import router as common_router

exception_handlers: list[ExceptionHandlerEntry] = [
    *auth_exception_handlers,
]

lifespans = [
    *common_lifespans,
]

routers = [
    auth_router,
    common_router,
]


app = FastAPI(lifespan=LifespanManager(lifespans))

for router in routers:
    app.include_router(router)

for exc, handler in exception_handlers:
    app.add_exception_handler(exc, handler)
