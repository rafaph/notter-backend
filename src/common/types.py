from typing import TypeAlias

from starlette.types import ExceptionHandler

ExceptionHandlerEntry: TypeAlias = tuple[type[Exception], ExceptionHandler]
