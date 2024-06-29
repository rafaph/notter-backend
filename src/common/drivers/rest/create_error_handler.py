from collections.abc import Mapping

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.types import ExceptionHandler


def create_error_handler(
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
