from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.types import ExceptionHandler

from src.auth.use_cases.errors import (
    EmailAlreadyExistsError,
    UserNotFoundError,
)


def _create_handler(
    status_code: int,
) -> ExceptionHandler:
    def handler(_request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={"detail": str(exc)},
        )

    return handler


exception_handlers: list[tuple[int | type[Exception], ExceptionHandler]] = [
    (UserNotFoundError, _create_handler(status.HTTP_404_NOT_FOUND)),
    (EmailAlreadyExistsError, _create_handler(status.HTTP_409_CONFLICT)),
]
