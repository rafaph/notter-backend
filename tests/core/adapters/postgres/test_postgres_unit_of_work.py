import pytest
from psycopg import AsyncConnection
from psycopg.rows import DictRow
from psycopg_pool import AsyncConnectionPool

from tests.auth.builders.domain.entities.user_builder import UserBuilder
from tests.core.builders.domain.entities.note_builder import NoteBuilder
from tests.core.helpers.core_database_client import CoreDatabaseClient

from src.core.adapters.postgres.postgres_unit_of_work import PostgresUnitOfWork


@pytest.mark.describe(PostgresUnitOfWork.__name__)
@pytest.mark.anyio(scope="class")
class TestPostgresUnitOfWork:
    @pytest.mark.it("Should persist the operation if commited")
    async def test_persist(
        self,
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        sut = PostgresUnitOfWork(pool)
        database_client = CoreDatabaseClient(pool)

        # and
        user = UserBuilder().build()
        await database_client.create_user(user)

        # and
        note = NoteBuilder().with_user_id(user.id).build()

        async with sut:
            await sut.note_repository.create(note)
            await sut.commit()

        # then
        note_from_db = await database_client.select_note(note.id)
        assert note_from_db == note

    @pytest.mark.it("Should not persist the operation if it is not commited")
    async def test_not_persist(
        self,
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        sut = PostgresUnitOfWork(pool)
        database_client = CoreDatabaseClient(pool)

        # and
        user = UserBuilder().build()
        await database_client.create_user(user)

        # and
        note = NoteBuilder().with_user_id(user.id).build()

        async with sut:
            await sut.note_repository.create(note)

        # then
        note_from_db = await database_client.select_note(note.id)
        assert note_from_db is None
