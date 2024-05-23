from typing import cast
from uuid import UUID, uuid4

import pytest
from faker import Faker
from psycopg import errors

from tests.auth.builders.domain.entities.user_builder import UserBuilder
from tests.auth.helpers.auth_database_client import AuthDatabaseClient
from tests.helpers.database_test import DatabaseTest

from src.auth.adapters.repositories.postgres.postgres_user_repository import (
    PostgresUserRepository,
)
from src.common.adapters.errors import DatabaseError


@pytest.mark.anyio(scope="class")
@pytest.mark.describe(PostgresUserRepository.__name__)
class TestPostgresUserRepository:
    @pytest.mark.it("Should create an user (return none)")
    async def test_create_user(self) -> None:
        async with DatabaseTest() as pool:
            # given
            user = UserBuilder().build()
            client = AuthDatabaseClient(pool)
            sut = PostgresUserRepository(pool)

            # when
            await sut.create(user)

            # then
            user_from_db = await client.select_user(user.id)
            assert user == user_from_db

    @pytest.mark.it("Should NOT create an user (raise database error)")
    async def test_create_raise_database_error(self) -> None:
        async with DatabaseTest() as pool:
            # given
            user = UserBuilder().build()
            client = AuthDatabaseClient(pool)
            await client.create_user(user)
            sut = PostgresUserRepository(pool)

            # when
            with pytest.raises(DatabaseError) as exc_info:
                await sut.create(user)

            # then
            error = exc_info.value
            assert isinstance(error.error, errors.UniqueViolation)
            assert str(error)

            # and
            unique_violation = "23505"
            assert error.error.diag.sqlstate == unique_violation

    @pytest.mark.it("Should find an user by email (return user)")
    async def test_find_by_email(self) -> None:
        async with DatabaseTest() as pool:
            # given
            client = AuthDatabaseClient(pool)
            user = UserBuilder().build()
            await client.create_user(user)

            # and
            sut = PostgresUserRepository(pool)

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
    ) -> None:
        async with DatabaseTest() as pool:
            # given
            email = faker.email()
            sut = PostgresUserRepository(pool)

            # when
            user_from_db = await sut.find_by_email(email)

            # then
            assert user_from_db is None

    @pytest.mark.it("Should NOT find an user by email (raise database error)")
    async def test_find_by_email_raise_database_error(
        self,
        faker: Faker,
    ) -> None:
        async with DatabaseTest() as pool:
            # given
            email = cast(str, faker.boolean())
            sut = PostgresUserRepository(pool)

            # when/then
            with pytest.raises(DatabaseError):
                await sut.find_by_email(email)

    @pytest.mark.it("Should find an user by id (return user)")
    async def test_find_by_id(self) -> None:
        async with DatabaseTest() as pool:
            # given
            client = AuthDatabaseClient(pool)
            user = UserBuilder().build()
            await client.create_user(user)

            # and
            sut = PostgresUserRepository(pool)

            # when
            user_from_db = await sut.find_by_id(user.id)

            # then
            assert user_from_db is not None

            # and
            assert user == user_from_db

    @pytest.mark.it("Should NOT find an user by id (return none)")
    async def test_find_by_id_return_none(self) -> None:
        async with DatabaseTest() as pool:
            # given
            user_id = uuid4()
            sut = PostgresUserRepository(pool)

            # when
            user_from_db = await sut.find_by_id(user_id)

            # then
            assert user_from_db is None

    @pytest.mark.it("Should NOT find an user by id (raise database error)")
    async def test_find_by_id_raise_database_error(
        self,
        faker: Faker,
    ) -> None:
        async with DatabaseTest() as pool:
            # given
            user_id = cast(UUID, faker.boolean())
            sut = PostgresUserRepository(pool)

            # when/then
            with pytest.raises(DatabaseError):
                await sut.find_by_id(user_id)
