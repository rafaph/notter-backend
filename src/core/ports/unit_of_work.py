from abc import ABC, abstractmethod
from collections.abc import Awaitable
from types import TracebackType
from typing import Self

from src.core.ports.repositories.category_repository import CategoryRepository
from src.core.ports.repositories.note_category_repository import (
    NoteCategoryRepository,
)
from src.core.ports.repositories.note_repository import NoteRepository


class UnitOfWork(ABC):
    note_repository: NoteRepository
    category_repository: CategoryRepository
    note_category_repository: NoteCategoryRepository

    @abstractmethod
    async def __aenter__(self) -> Self:
        raise NotImplementedError  # pragma: no cover

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.rollback()

    @abstractmethod
    def commit(self) -> Awaitable[None]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def rollback(self) -> Awaitable[None]:
        raise NotImplementedError  # pragma: no cover
