from uuid import UUID

from psycopg import AsyncConnection, errors
from psycopg.rows import DictRow

from src.common.adapters.errors import DatabaseError
from src.core.domain.entities import Category
from src.core.ports.repositories.category_repository import CategoryRepository


class PostgresCategoryRepository(CategoryRepository):
    def __init__(self, connection: AsyncConnection[DictRow]) -> None:
        self._connection = connection

    async def create(self, category: Category) -> None:
        try:
            async with self._connection.cursor() as cursor:
                await cursor.execute(
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
        except errors.Error as error:
            raise DatabaseError(error) from error

    async def update(
        self,
        category: Category,
    ) -> None:
        try:
            async with self._connection.cursor() as cursor:
                await cursor.execute(
                    """
                    UPDATE categories
                    SET
                        user_id = %(user_id)s,
                        name = %(name)s,
                        updated_at = %(updated_at)s,
                        created_at = %(created_at)s
                    WHERE id = %(id)s;
                    """,
                    category.model_dump(),
                )
        except errors.Error as error:
            raise DatabaseError(error) from error

    async def delete(
        self,
        category_id: UUID,
    ) -> None:
        try:
            async with self._connection.cursor() as cursor:
                await cursor.execute(
                    """
                    DELETE FROM categories
                    WHERE id = %s;
                    """,
                    [category_id],
                )
        except errors.Error as error:
            raise DatabaseError(error) from error
