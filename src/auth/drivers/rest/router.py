from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.auth.drivers.rest.dependencies import (
    get_authenticate_input,
    get_authenticate_use_case,
    get_create_user_use_case,
)
from src.auth.use_cases.authenticate_use_case import AuthenticateUseCase
from src.auth.use_cases.create_user_use_case import CreateUserUseCase
from src.auth.use_cases.inputs import AuthenticateInput, CreateUserInput
from src.auth.use_cases.output import AuthenticateOutput, CreateUserOutput
from src.common.drivers.rest.errors import ErrorResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateUserOutput,
    summary="Create a new user",
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
async def post_signup(
    data: CreateUserInput,
    create_user: Annotated[
        CreateUserUseCase,
        Depends(get_create_user_use_case),
    ],
) -> CreateUserOutput:
    return await create_user(data)


@router.post(
    "/token",
    status_code=status.HTTP_200_OK,
    response_model=AuthenticateOutput,
    summary="Generate a token",
    responses={
        status.HTTP_200_OK: {
            "description": "User authenticated successfully",
            "model": AuthenticateOutput,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
            "model": ErrorResponse,
        },
    },
)
async def post_token(
    data: Annotated[
        AuthenticateInput,
        Depends(get_authenticate_input),
    ],
    authenticate: Annotated[
        AuthenticateUseCase,
        Depends(get_authenticate_use_case),
    ],
) -> AuthenticateOutput:
    return await authenticate(data)
