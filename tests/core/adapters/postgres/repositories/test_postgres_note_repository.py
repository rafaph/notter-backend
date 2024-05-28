import pytest
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

        # when/then
        await sut.create(note)

        # and
        await connection.commit()

        # and
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
