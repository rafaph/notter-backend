from typing import cast
from uuid import UUID, uuid4

import pytest
from faker import Faker
from psycopg import AsyncConnection, errors
from psycopg.rows import DictRow
from psycopg_pool import AsyncConnectionPool

from tests.auth.builders.domain.entities.user_builder import UserBuilder
from tests.auth.helpers.auth_database_client import AuthDatabaseClient

from src.auth.adapters.repositories.postgres.postgres_user_repository import (
    PostgresUserRepository,
)
from src.common.adapters.errors import DatabaseError


@pytest.mark.anyio(scope="class")
@pytest.mark.describe(PostgresUserRepository.__name__)
class TestPostgresUserRepository:
    @pytest.mark.it("Should create an user (return none)")
    async def test_create_user(
        self,
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        client = AuthDatabaseClient(pool)
        sut = PostgresUserRepository(pool)

        # and
        user = UserBuilder().build()

        # when
        await sut.create(user)

        # then
        user_from_db = await client.select_user(user.id)
        assert user == user_from_db

    @pytest.mark.it("Should NOT create an user (raise database error)")
    async def test_create_raise_database_error(
        self,
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        client = AuthDatabaseClient(pool)
        sut = PostgresUserRepository(pool)

        # and
        user = UserBuilder().build()
        await client.create_user(user)

        # when/then
        with pytest.raises(DatabaseError) as exc_info:
            await sut.create(user)

        # and
        error = exc_info.value
        assert isinstance(error.error, errors.UniqueViolation)
        assert str(error)

        # and
        unique_violation = "23505"
        assert error.error.diag.sqlstate == unique_violation

    @pytest.mark.it("Should find an user by email (return user)")
    async def test_find_by_email(
        self,
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        client = AuthDatabaseClient(pool)
        sut = PostgresUserRepository(pool)

        # and
        user = UserBuilder().build()
        await client.create_user(user)

        # when
        user_from_db = await sut.find_by_email(user.email)

        # then
        assert user_from_db is not None

        # and
        assert user == user_from_db

    @pytest.mark.it("Should NOT find an user by email (return none)")
    async def test_find_by_email_return_none(
        self,
        faker: Faker,
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        sut = PostgresUserRepository(pool)

        # and
        email = faker.email()

        # when
        user_from_db = await sut.find_by_email(email)

        # then
        assert user_from_db is None

    @pytest.mark.it("Should NOT find an user by email (raise database error)")
    async def test_find_by_email_raise_database_error(
        self,
        faker: Faker,
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        sut = PostgresUserRepository(pool)

        # and
        email = cast(str, faker.boolean())

        # when/then
        with pytest.raises(DatabaseError):
            await sut.find_by_email(email)

    @pytest.mark.it("Should find an user by id (return user)")
    async def test_find_by_id(
        self,
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        client = AuthDatabaseClient(pool)
        sut = PostgresUserRepository(pool)

        # and
        user = UserBuilder().build()
        await client.create_user(user)

        # when
        user_from_db = await sut.find_by_id(user.id)

        # then
        assert user_from_db is not None

        # and
        assert user == user_from_db

    @pytest.mark.it("Should NOT find an user by id (return none)")
    async def test_find_by_id_return_none(
        self,
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        sut = PostgresUserRepository(pool)

        # and
        user_id = uuid4()

        # when
        user_from_db = await sut.find_by_id(user_id)

        # then
        assert user_from_db is None

    @pytest.mark.it("Should NOT find an user by id (raise database error)")
    async def test_find_by_id_raise_database_error(
        self,
        faker: Faker,
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        sut = PostgresUserRepository(pool)

        # and
        user_id = cast(UUID, faker.boolean())

        # when/then
        with pytest.raises(DatabaseError):
            await sut.find_by_id(user_id)

    @pytest.mark.it("Should update an user (return none)")
    async def test_update(
        self,
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        client = AuthDatabaseClient(pool)
        sut = PostgresUserRepository(pool)

        # and
        user = UserBuilder().build()
        await client.create_user(user)

        # and
        user_to_update = UserBuilder().with_id(user.id).build()

        # when
        await sut.update(user_to_update)

        # then
        user_from_db = await client.select_user(user.id)

        # and
        assert user_to_update == user_from_db

    @pytest.mark.it("Should NOT update an user (raise database error)")
    async def test_update_database_error(
        self,
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        client = AuthDatabaseClient(pool)
        sut = PostgresUserRepository(pool)

        # and
        user = UserBuilder().build()
        await client.create_user(user)

        # and
        current_user = UserBuilder().build()
        await client.create_user(current_user)

        # and
        user_to_update = (
            UserBuilder()
            .with_id(current_user.id)
            .with_email(user.email)
            .build()
        )

        # when/then
        with pytest.raises(DatabaseError) as exc_info:
            await sut.update(user_to_update)

        # and
        error = exc_info.value
        assert isinstance(error.error, errors.UniqueViolation)
        assert str(error)

        # and
        unique_violation = "23505"
        assert error.error.diag.sqlstate == unique_violation
