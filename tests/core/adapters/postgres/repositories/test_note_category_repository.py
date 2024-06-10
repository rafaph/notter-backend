import pytest
from psycopg import AsyncConnection, errors
from psycopg.rows import DictRow
from psycopg_pool import AsyncConnectionPool

from tests.auth.builders.domain.entities.user_builder import UserBuilder
from tests.core.builders.domain.entities.category_builder import (
    CategoryBuilder,
)
from tests.core.builders.domain.entities.note_builder import NoteBuilder
from tests.core.builders.domain.entities.note_category_builder import (
    NoteCategoryBuilder,
)
from tests.core.helpers.core_database_client import CoreDatabaseClient

from src.common.adapters.errors import DatabaseError
from src.core.adapters.postgres.repositories import (
    PostgresNoteCategoryRepository,
)


@pytest.mark.describe(PostgresNoteCategoryRepository.__name__)
@pytest.mark.anyio(scope="class")
class TestPostgresNoteCategoryRepository:
    @pytest.mark.it("Should create a note-category")
    async def test_create(
        self,
        connection: AsyncConnection[DictRow],
        pool: AsyncConnectionPool[AsyncConnection[DictRow]],
    ) -> None:
        # given
        sut = PostgresNoteCategoryRepository(connection)
        database_client = CoreDatabaseClient(pool)

        # and
        user = UserBuilder().build()
        note = NoteBuilder().with_user_id(user.id).build()
        category = CategoryBuilder().with_user_id(user.id).build()
        await database_client.create_user(user)
        await database_client.create_note(note)
        await database_client.create_category(category)

        # and
        note_category = (
            NoteCategoryBuilder()
            .with_note_id(note.id)
            .with_category_id(category.id)
            .build()
        )

        # when
        await sut.create(note_category)

        # and
        await connection.commit()

        # then
        note_category_from_db = await database_client.select_note_category(
            note.id,
            category.id,
        )
        assert note_category_from_db == note_category

    @pytest.mark.it(
        "Should not create note-category if note or category does not exist"
    )
    async def test_not_create_foreign_key_violation(
        self,
        connection: AsyncConnection[DictRow],
    ) -> None:
        # given
        sut = PostgresNoteCategoryRepository(connection)

        # and
        note_category = NoteCategoryBuilder().build()

        # when/then
        with pytest.raises(DatabaseError) as exc_info:
            await sut.create(note_category)

        # and
        assert isinstance(exc_info.value.error, errors.ForeignKeyViolation)
