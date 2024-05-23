from uuid import UUID

from psycopg import errors

from src.auth.domain.entities.user import User
from src.auth.ports.repositories.user_repository import UserRepository
from src.common.adapters.errors import DatabaseError
from src.common.adapters.postgres.postgres_repository import PostgresRepository


class PostgresUserRepository(PostgresRepository, UserRepository):
    async def create(self, user: User) -> None:
        try:
            await self._query(
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
        except errors.Error as error:
            raise DatabaseError(error) from error

    async def find_by_email(self, email: str) -> User | None:
        try:
            cursor = await self._query(
                "SELECT * FROM users WHERE email = %s;",
                [email],
            )
            result = await cursor.fetchall()
        except errors.Error as error:
            raise DatabaseError(error) from error

        if len(result) == 0:
            return None

        return User.model_validate(result[0])

    async def find_by_id(self, user_id: UUID) -> User | None:
        try:
            cursor = await self._query(
                "SELECT * FROM users WHERE id = %s;",
                [user_id],
            )
            result = await cursor.fetchall()
        except errors.Error as error:
            raise DatabaseError(error) from error

        if len(result) == 0:
            return None

        return User.model_validate(result[0])
