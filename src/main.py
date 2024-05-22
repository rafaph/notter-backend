import os

if os.getenv("TESTING") == "true":  # pragma: no cover
    from pytest_cov.embed import cleanup_on_sigterm  # type: ignore

    cleanup_on_sigterm()

from fastapi import FastAPI, status

from src.auth.drivers.rest.exception_handlers import (
    exception_handlers as auth_exception_handlers,
)
from src.auth.drivers.rest.router import router as auth_router
from src.common.drivers.rest.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)

exception_handlers = [
    *auth_exception_handlers,
]

for exc, handler in exception_handlers:
    app.add_exception_handler(exc, handler)


@app.get(
    "/healthz",
    tags=["common"],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Health check",
    description="Health check operation",
    response_description="Health checked successfully",
)
async def healthz() -> None: ...
