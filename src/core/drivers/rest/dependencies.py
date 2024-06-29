from typing import Annotated

from fastapi import Body, Depends
from psycopg import AsyncConnection
from psycopg.rows import DictRow
from psycopg_pool import AsyncConnectionPool

from src.auth.domain.entities import User
from src.auth.drivers.rest.dependencies import get_current_user
from src.common.drivers.rest.dependencies import get_pool
from src.common.drivers.rest.model_validate import model_validate
from src.core.adapters.postgres.postgres_unit_of_work import PostgresUnitOfWork
from src.core.ports.unit_of_work import UnitOfWork
from src.core.use_cases.create_category_use_case import CreateCategoryUseCase
from src.core.use_cases.inputs import (
    CreateCategoryInput,
    CreateCategoryInputBase,
)


def get_unit_of_work(
    pool: Annotated[
        AsyncConnectionPool[AsyncConnection[DictRow]],
        Depends(get_pool),
    ],
) -> UnitOfWork:
    return PostgresUnitOfWork(pool)


def get_create_category_use_case(
    unit_of_work: Annotated[
        UnitOfWork,
        Depends(get_unit_of_work),
    ],
) -> CreateCategoryUseCase:
    return CreateCategoryUseCase(unit_of_work)


async def get_create_category_input(
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    data: Annotated[
        CreateCategoryInputBase,
        Body(title="CreateCategoryInput"),
    ],
) -> CreateCategoryInput:
    return model_validate(
        CreateCategoryInput,
        {
            **data.model_dump(),
            "user_id": user.id,
        },
    )
