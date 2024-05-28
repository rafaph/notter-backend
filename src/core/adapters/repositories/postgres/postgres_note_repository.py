from psycopg import AsyncConnection, errors
from psycopg.rows import DictRow

from src.common.adapters.errors import DatabaseError
from src.core.domain.entities import Note
from src.core.ports.repositories.note_repository import NoteRepository


class PostgresNoteRepository(NoteRepository):
    def __init__(self, connection: AsyncConnection[DictRow]) -> None:
        self._connection = connection

    async def create(self, note: Note) -> None:
        try:
            async with self._connection.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO notes (
                        id,
                        user_id,
                        title,
                        content,
                        updated_at,
                        created_at
                    ) VALUES (
                        %(id)s,
                        %(user_id)s,
                        %(title)s,
                        %(content)s,
                        %(updated_at)s,
                        %(created_at)s
                    );
                    """,
                    note.model_dump(),
                )
        except errors.Error as error:
            raise DatabaseError(error) from error
