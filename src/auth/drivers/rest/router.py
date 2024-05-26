from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.auth.domain.entities import User
from src.auth.drivers.rest.dependencies import (
    get_authenticate_input,
    get_authenticate_use_case,
    get_create_user_use_case,
    get_current_user,
    get_update_user_use_case,
)
from src.auth.use_cases.authenticate_use_case import AuthenticateUseCase
from src.auth.use_cases.create_user_use_case import CreateUserUseCase
from src.auth.use_cases.inputs import (
    AuthenticateInput,
    CreateUserInput,
    UpdateUserInput,
)
from src.auth.use_cases.output import (
    AuthenticateOutput,
    CreateUserOutput,
    GetProfileOutput,
    UpdateUserOutput,
)
from src.auth.use_cases.update_user_use_case import UpdateUserUseCase
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


@router.get(
    "/profile",
    status_code=status.HTTP_200_OK,
    response_model=GetProfileOutput,
    summary="Get authenticated user profile",
    responses={
        status.HTTP_200_OK: {
            "description": "User profile data",
            "model": GetProfileOutput,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Not authorized",
            "model": ErrorResponse,
        },
    },
)
def get_profile(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
) -> GetProfileOutput:
    return GetProfileOutput.from_user(current_user)


@router.post(
    "/profile",
    status_code=status.HTTP_200_OK,
    response_model=GetProfileOutput,
    summary="Update authenticated user profile",
    responses={
        status.HTTP_200_OK: {
            "description": "User updated profile data",
            "model": UpdateUserOutput,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Not authorized",
            "model": ErrorResponse,
        },
        status.HTTP_409_CONFLICT: {
            "description": "Email already in use",
            "model": ErrorResponse,
        },
    },
)
async def post_profile(
    data: UpdateUserInput,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    update_user: Annotated[
        UpdateUserUseCase,
        Depends(get_update_user_use_case),
    ],
) -> UpdateUserOutput:
    return await update_user(current_user, data)
