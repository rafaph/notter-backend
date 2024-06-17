from typing import Any, TypeAlias, TypeVar

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)

DataType: TypeAlias = Any  # type: ignore[misc]


def model_validate(
    model_class: type[T],
    data: DataType,
    *,
    strict: bool | None = None,
    base_loc: tuple[str, ...] = ("body",),
    include_input: bool = False,
) -> T:
    try:
        return model_class.model_validate(
            data,
            strict=strict,
        )
    except ValidationError as validation_error:
        errors = validation_error.errors(
            include_input=include_input,
            include_url=False,
        )

        for error in errors:
            error["loc"] = (*base_loc, *error["loc"])

        raise RequestValidationError(errors) from validation_error
