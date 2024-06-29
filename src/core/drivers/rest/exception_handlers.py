from fastapi import status

from src.common.drivers.rest.create_error_handler import create_error_handler
from src.common.types import ExceptionHandlerEntry
from src.core.use_cases.errors import CategoryAlreadyExistsError

exception_handlers: list[ExceptionHandlerEntry] = [
    (
        CategoryAlreadyExistsError,
        create_error_handler(status.HTTP_409_CONFLICT),
    ),
]
