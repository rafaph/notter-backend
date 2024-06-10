from uuid import UUID

from tests.auth.helpers.auth_database_client import AuthDatabaseClient

from src.core.domain.entities import Category, Note, NoteCategory


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

    async def select_category(self, category_id: UUID) -> Category | None:
        cursor = await self.query(
            "SELECT * FROM categories WHERE id = %s;",
            [category_id],
        )

        result = await cursor.fetchall()

        if len(result) == 0:
            return None

        return Category.model_validate(result[0])

    async def create_category(self, category: Category) -> None:
        await self.query(
            """
            INSERT INTO categories (
                id,
                user_id,
                name,
                updated_at,
                created_at
            ) VALUES (
                %(id)s,
                %(user_id)s,
                %(name)s,
                %(updated_at)s,
                %(created_at)s
            );
            """,
            category.model_dump(),
        )

    async def select_note_category(
        self,
        note_id: UUID,
        category_id: UUID,
    ) -> NoteCategory | None:
        cursor = await self.query(
            """
            SELECT * FROM notes_categories
            WHERE
                note_id = %s AND
                category_id = %s;
            """,
            [note_id, category_id],
        )

        result = await cursor.fetchall()

        if len(result) == 0:
            return None

        return NoteCategory.model_validate(result[0])
