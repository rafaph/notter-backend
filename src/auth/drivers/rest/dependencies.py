from functools import cache
from typing import Annotated

import argon2
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from psycopg import AsyncConnection
from psycopg.rows import DictRow
from psycopg_pool import AsyncConnectionPool

from src.auth.adapters.argon2_password_hasher import Argon2PasswordHasher
from src.auth.adapters.py_jwt_manager import PyJwtManager
from src.auth.adapters.repositories.postgres.postgres_user_repository import (
    PostgresUserRepository,
)
from src.auth.ports.jwt_manager import JwtManager
from src.auth.ports.password_hasher import PasswordHasher
from src.auth.ports.repositories.user_repository import UserRepository
from src.auth.use_cases.authenticate_use_case import AuthenticateUseCase
from src.auth.use_cases.create_user_use_case import CreateUserUseCase
from src.auth.use_cases.inputs import AuthenticateInput
from src.common.drivers.rest.dependencies import get_pool
from src.common.settings import settings


@cache
def get_password_hasher() -> PasswordHasher:
    argon2_password_hasher = argon2.PasswordHasher()
    return Argon2PasswordHasher(
        argon2_password_hasher,
    )


@cache
def get_user_repository(
    pool: Annotated[
        AsyncConnectionPool[AsyncConnection[DictRow]],
        Depends(get_pool),
    ],
) -> UserRepository:
    return PostgresUserRepository(pool)


@cache
def get_create_user_use_case(
    user_repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
    password_hasher: Annotated[
        PasswordHasher,
        Depends(get_password_hasher),
    ],
) -> CreateUserUseCase:
    return CreateUserUseCase(
        user_repository,
        password_hasher,
    )


@cache
def get_jwt_manager() -> JwtManager:
    return PyJwtManager(
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )


@cache
def get_authenticate_use_case(
    user_repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
    jwt_manager: Annotated[
        JwtManager,
        Depends(get_jwt_manager),
    ],
    password_hasher: Annotated[
        PasswordHasher,
        Depends(get_password_hasher),
    ],
) -> AuthenticateUseCase:
    return AuthenticateUseCase(
        user_repository,
        jwt_manager,
        password_hasher,
    )


def get_authenticate_input(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
) -> AuthenticateInput:
    return AuthenticateInput(
        email=form_data.username,
        password=form_data.password,
    )
