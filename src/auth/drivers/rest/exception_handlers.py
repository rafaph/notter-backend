from fastapi import status

from src.auth.use_cases.errors import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
)
from src.common.drivers.rest.create_error_handler import create_error_handler
from src.common.types import ExceptionHandlerEntry

exception_handlers: list[ExceptionHandlerEntry] = [
    (
        EmailAlreadyExistsError,
        create_error_handler(status.HTTP_409_CONFLICT),
    ),
    (
        InvalidCredentialsError,
        create_error_handler(
            status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        ),
    ),
    (
        InvalidTokenError,
        create_error_handler(
            status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        ),
    ),
]
