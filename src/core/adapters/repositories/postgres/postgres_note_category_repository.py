from psycopg import AsyncConnection, errors
from psycopg.rows import DictRow

from src.common.adapters.errors import DatabaseError
from src.core.domain.entities import NoteCategory
from src.core.ports.repositories.note_category_repository import (
    NoteCategoryRepository,
)


class PostgresNoteRepository(NoteCategoryRepository):
    def __init__(self, connection: AsyncConnection[DictRow]) -> None:
        self._connection = connection

    async def create(self, note_category: NoteCategory) -> None:
        await self.create_many([note_category])

    async def create_many(
        self,
        notes_categories: list[NoteCategory],
    ) -> None:
        try:
            async with self._connection.cursor() as cursor:
                await cursor.executemany(
                    """
                    INSERT INTO notes_categories (
                        note_id,
                        category_id,
                        updated_at,
                        created_at,
                    ) VALUES (
                        %(note_id)s,
                        %(category_id)s,
                        %(updated_at)s,
                        %(created_at)s
                    );
                    """,
                    (
                        note_category.model_dump()
                        for note_category in notes_categories
                    ),
                )
        except errors.Error as error:
            raise DatabaseError(error) from error
