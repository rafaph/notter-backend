from uuid import UUID

from tests.helpers.database_client import DatabaseClient

from src.auth.domain.entities import User


class AuthDatabaseClient(DatabaseClient):
    async def create_user(self, user: User) -> None:
        await self.query(
            """
            INSERT INTO users (
                id,
                email,
                password,
                first_name,
                last_name,
                updated_at,
                created_at
            ) VALUES (
                %(id)s,
                %(email)s,
                %(password)s,
                %(first_name)s,
                %(last_name)s,
                %(updated_at)s,
                %(created_at)s
            );
            """,
            user.model_dump(),
        )

    async def select_user(self, id_: UUID | str) -> User | None:
        cursor = await self.query(
            "SELECT * FROM users WHERE id = %s;",
            [id_],
        )

        result = await cursor.fetchall()

        if len(result) == 0:
            return None

        return User.model_validate(result[0])
