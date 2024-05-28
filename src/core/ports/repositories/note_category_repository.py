from abc import ABC, abstractmethod
from collections.abc import Awaitable

from src.core.domain.entities import NoteCategory


class NoteCategoryRepository(ABC):
    @abstractmethod
    def create(
        self,
        note_category: NoteCategory,
    ) -> Awaitable[None]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def create_many(
        self,
        note_categories: list[NoteCategory],
    ) -> Awaitable[None]:
        raise NotImplementedError  # pragma: no cover
