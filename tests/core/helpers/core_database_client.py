from uuid import UUID

from tests.auth.helpers.auth_database_client import AuthDatabaseClient

from src.core.domain.entities import Note


class CoreDatabaseClient(AuthDatabaseClient):
    async def select_note(self, note_id: UUID) -> Note | None:
        cursor = await self.query(
            "SELECT * FROM notes WHERE id = %s;",
            [note_id],
        )

        result = await cursor.fetchall()

        if len(result) == 0:
            return None

        return Note.model_validate(result[0])

    async def create_note(self, note: Note) -> None:
        await self.query(
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
