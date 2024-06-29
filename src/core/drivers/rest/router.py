from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.common.drivers.rest.errors import ErrorResponse
from src.core.drivers.rest.dependencies import (
    get_create_category_input,
    get_create_category_use_case,
)
from src.core.use_cases.create_category_use_case import CreateCategoryUseCase
from src.core.use_cases.inputs import CreateCategoryInput
from src.core.use_cases.outputs import CreateCategoryOutput

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateCategoryOutput,
    summary="Create a new category",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Category created successfully",
            "model": CreateCategoryOutput,
        },
        status.HTTP_409_CONFLICT: {
            "description": "Category already exists",
            "model": ErrorResponse,
        },
    },
)
async def post_categories(
    data: Annotated[
        CreateCategoryInput,
        Depends(get_create_category_input),
    ],
    create_category: Annotated[
        CreateCategoryUseCase,
        Depends(get_create_category_use_case),
    ],
) -> CreateCategoryOutput:
    return await create_category(data)
