from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.auth.drivers.rest.dependencies import get_create_user_use_case
from src.auth.use_cases.create_user_use_case import CreateUserUseCase
from src.auth.use_cases.inputs import CreateUserInput
from src.auth.use_cases.output import CreateUserOutput
from src.common.drivers.rest.errors import ErrorResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateUserOutput,
    description="Create a new user",
    responses={
        status.HTTP_201_CREATED: {
            "description": "User created successfully",
            "model": CreateUserOutput,
        },
        status.HTTP_409_CONFLICT: {
            "description": "Email already in use",
            "model": ErrorResponse,
        },
    },
)
async def signup(
    data: CreateUserInput,
    create_user: Annotated[
        CreateUserUseCase,
        Depends(get_create_user_use_case),
    ],
) -> CreateUserOutput:
    return await create_user(data)
