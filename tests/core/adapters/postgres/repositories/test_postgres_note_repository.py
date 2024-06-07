from typing import cast
from uuid import UUID

import pytest
from faker import Faker
from psycopg import AsyncConnection, errors
from psycopg.rows import DictRow
from psycopg_pool import AsyncConnectionPool

from tests.auth.builders.domain.entities.user_builder import UserBuilder
from tests.core.builders.domain.entities.note_builder import NoteBuilder
from tests.core.helpers.core_database_client import CoreDatabaseClient

from src.common.adapters.errors import DatabaseError
from src.core.adapters.postgres.repositories import (
    PostgresNoteRepository,
)


@pytest.mark.describe(PostgresNoteRepository.__name__)
@pytest.mark.anyio(scope="class")
class TestPostgresNoteRepository:
    @pytest.mark.it("Should create a note")
    async def test_create(
        self,
        connection: AsyncConnection[DictRow],
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        sut = PostgresNoteRepository(connection)
        database_client = CoreDatabaseClient(pool)

        # and
        user = UserBuilder().build()
        await database_client.create_user(user)

        # and
        note = NoteBuilder().with_user_id(user.id).build()

        # when
        await sut.create(note)

        # and
        await connection.commit()

        # then
        note_from_db = await database_client.select_note(note.id)
        assert note_from_db == note

    @pytest.mark.it("Should not create note if user does not exist")
    async def test_not_create_foreign_key_violation(
        self,
        connection: AsyncConnection[DictRow],
    ) -> None:
        # given
        sut = PostgresNoteRepository(connection)

        # and
        note = NoteBuilder().build()

        # when/then
        with pytest.raises(DatabaseError) as exc_info:
            await sut.create(note)

        # and
        assert isinstance(exc_info.value.error, errors.ForeignKeyViolation)

    @pytest.mark.it("Should update a note")
    async def test_update(
        self,
        connection: AsyncConnection[DictRow],
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        sut = PostgresNoteRepository(connection)
        database_client = CoreDatabaseClient(pool)

        # and
        user = UserBuilder().build()
        await database_client.create_user(user)

        # and
        note = NoteBuilder().with_user_id(user.id).build()
        await database_client.create_note(note)

        # and
        note_to_update = (
            NoteBuilder().with_id(note.id).with_user_id(user.id).build()
        )

        # when
        await sut.update(note_to_update)

        # and
        await connection.commit()

        # then
        note_from_db = await database_client.select_note(note.id)
        assert note_to_update == note_from_db

    @pytest.mark.it("Should not update note if user does not exist")
    async def test_not_update_foreign_key_violation(
        self,
        connection: AsyncConnection[DictRow],
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        sut = PostgresNoteRepository(connection)
        database_client = CoreDatabaseClient(pool)

        # and
        user = UserBuilder().build()
        await database_client.create_user(user)

        # and
        note = NoteBuilder().with_user_id(user.id).build()
        await database_client.create_note(note)

        # and
        note_to_update = NoteBuilder().with_id(note.id).build()

        # when/then
        with pytest.raises(DatabaseError) as exc_info:
            await sut.update(note_to_update)

        # and
        assert isinstance(exc_info.value.error, errors.ForeignKeyViolation)

    @pytest.mark.it("Should delete a note")
    async def test_delete_note(
        self,
        connection: AsyncConnection[DictRow],
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        sut = PostgresNoteRepository(connection)
        database_client = CoreDatabaseClient(pool)

        # and
        user = UserBuilder().build()
        await database_client.create_user(user)

        # and
        note = NoteBuilder().with_user_id(user.id).build()
        await database_client.create_note(note)

        # when
        await sut.delete(note.id)

        # and
        await connection.commit()

        # then
        note_from_db = await database_client.select_note(note.id)
        assert note_from_db is None

    @pytest.mark.it("Should not delete a note if it does not exist")
    async def test_not_delete_note(
        self,
        connection: AsyncConnection[DictRow],
        faker: Faker,
    ) -> None:
        # given
        sut = PostgresNoteRepository(connection)

        # and
        note_id = cast(UUID, faker.random_int())

        # when/then
        with pytest.raises(DatabaseError) as exc_info:
            await sut.delete(note_id)

        # and
        assert isinstance(exc_info.value.error, errors.ProgrammingError)
