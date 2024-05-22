from functools import cache
from typing import Annotated

import argon2
from fastapi import Depends
from psycopg import AsyncConnection
from psycopg.rows import DictRow
from psycopg_pool import AsyncConnectionPool

from src.auth.adapters.argon2_password_hasher import Argon2PasswordHasher
from src.auth.adapters.repositories.postgres.postgres_user_repository import (
    PostgresUserRepository,
)
from src.auth.ports.password_hasher import PasswordHasher
from src.auth.ports.repositories.user_repository import UserRepository
from src.auth.use_cases.create_user_use_case import CreateUserUseCase
from src.common.drivers.rest.dependencies import get_pool


@cache
def get_password_hasher() -> PasswordHasher:
    argon2_password_hasher = argon2.PasswordHasher()
    return Argon2PasswordHasher(argon2_password_hasher)


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
    password_hasher: Annotated[
        PasswordHasher,
        Depends(get_password_hasher),
    ],
    user_repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> CreateUserUseCase:
    return CreateUserUseCase(user_repository, password_hasher)
