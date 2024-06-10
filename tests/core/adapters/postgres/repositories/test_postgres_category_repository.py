from typing import cast
from uuid import UUID

import pytest
from faker import Faker
from psycopg import AsyncConnection, errors
from psycopg.rows import DictRow
from psycopg_pool import AsyncConnectionPool

from tests.auth.builders.domain.entities.user_builder import UserBuilder
from tests.core.builders.domain.entities.category_builder import (
    CategoryBuilder,
)
from tests.core.helpers.core_database_client import CoreDatabaseClient

from src.common.adapters.errors import DatabaseError
from src.core.adapters.postgres.repositories import (
    PostgresCategoryRepository,
)


@pytest.mark.describe(PostgresCategoryRepository.__name__)
@pytest.mark.anyio(scope="class")
class TestPostgresCategoryRepository:
    @pytest.mark.it("Should create a category")
    async def test_create(
        self,
        connection: AsyncConnection[DictRow],
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        sut = PostgresCategoryRepository(connection)
        database_client = CoreDatabaseClient(pool)

        # and
        user = UserBuilder().build()
        await database_client.create_user(user)

        # and
        category = CategoryBuilder().with_user_id(user.id).build()

        # when
        await sut.create(category)

        # and
        await connection.commit()

        # then
        category_from_db = await database_client.select_category(category.id)
        assert category_from_db == category

    @pytest.mark.it("Should not create category if user does not exist")
    async def test_not_create_foreign_key_violation(
        self,
        connection: AsyncConnection[DictRow],
    ) -> None:
        # given
        sut = PostgresCategoryRepository(connection)

        # and
        category = CategoryBuilder().build()

        # when/then
        with pytest.raises(DatabaseError) as exc_info:
            await sut.create(category)

        # and
        assert isinstance(exc_info.value.error, errors.ForeignKeyViolation)

    @pytest.mark.it("Should update a category")
    async def test_update(
        self,
        connection: AsyncConnection[DictRow],
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        sut = PostgresCategoryRepository(connection)
        database_client = CoreDatabaseClient(pool)

        # and
        user = UserBuilder().build()
        await database_client.create_user(user)

        # and
        category = CategoryBuilder().with_user_id(user.id).build()
        await database_client.create_category(category)

        # and
        category_to_update = (
            CategoryBuilder()
            .with_id(category.id)
            .with_user_id(user.id)
            .build()
        )

        # when
        await sut.update(category_to_update)

        # and
        await connection.commit()

        # then
        category_from_db = await database_client.select_category(category.id)
        assert category_to_update == category_from_db

    @pytest.mark.it("Should not update category if user does not exist")
    async def test_not_update_foreign_key_violation(
        self,
        connection: AsyncConnection[DictRow],
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        sut = PostgresCategoryRepository(connection)
        database_client = CoreDatabaseClient(pool)

        # and
        user = UserBuilder().build()
        await database_client.create_user(user)

        # and
        category = CategoryBuilder().with_user_id(user.id).build()
        await database_client.create_category(category)

        # and
        category_to_update = CategoryBuilder().with_id(category.id).build()

        # when/then
        with pytest.raises(DatabaseError) as exc_info:
            await sut.update(category_to_update)

        # and
        assert isinstance(exc_info.value.error, errors.ForeignKeyViolation)

    @pytest.mark.it("Should delete a category")
    async def test_delete_category(
        self,
        connection: AsyncConnection[DictRow],
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        sut = PostgresCategoryRepository(connection)
        database_client = CoreDatabaseClient(pool)

        # and
        user = UserBuilder().build()
        await database_client.create_user(user)

        # and
        category = CategoryBuilder().with_user_id(user.id).build()
        await database_client.create_category(category)

        # when
        await sut.delete(category.id)

        # and
        await connection.commit()

        # then
        category_from_db = await database_client.select_category(category.id)
        assert category_from_db is None

    @pytest.mark.it("Should not delete a category if it does not exist")
    async def test_not_delete_category(
        self,
        connection: AsyncConnection[DictRow],
        faker: Faker,
    ) -> None:
        # given
        sut = PostgresCategoryRepository(connection)

        # and
        category_id = cast(UUID, faker.random_int())

        # when/then
        with pytest.raises(DatabaseError) as exc_info:
            await sut.delete(category_id)

        # and
        assert isinstance(exc_info.value.error, errors.ProgrammingError)
