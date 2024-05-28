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
