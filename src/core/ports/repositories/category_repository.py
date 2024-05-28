from abc import ABC, abstractmethod
from collections.abc import Awaitable
from uuid import UUID

from src.core.domain.entities import Category


class CategoryRepository(ABC):
    @abstractmethod
    def create(
        self,
        category: Category,
    ) -> Awaitable[None]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def update(
        self,
        category: Category,
    ) -> Awaitable[None]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def delete(
        self,
        category_id: UUID,
    ) -> Awaitable[None]:
        raise NotImplementedError  # pragma: no cover
