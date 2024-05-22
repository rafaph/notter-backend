from collections.abc import Mapping

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.types import ExceptionHandler

from src.auth.use_cases.errors import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from src.common.types import ExceptionHandlerEntry


def _create_handler(
    status_code: int,
    *,
    headers: Mapping[str, str] | None = None,
) -> ExceptionHandler:
    def handler(_request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={"detail": str(exc)},
            headers=headers,
        )

    return handler


exception_handlers: list[ExceptionHandlerEntry] = [
    (
        UserNotFoundError,
        _create_handler(status.HTTP_404_NOT_FOUND),
    ),
    (
        EmailAlreadyExistsError,
        _create_handler(status.HTTP_409_CONFLICT),
    ),
    (
        InvalidCredentialsError,
        _create_handler(
            status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        ),
    ),
]
