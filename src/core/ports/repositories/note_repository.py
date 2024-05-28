from abc import ABC, abstractmethod
from collections.abc import Awaitable
from uuid import UUID

from src.core.domain.entities import Note


class NoteRepository(ABC):
    @abstractmethod
    def create(
        self,
        note: Note,
    ) -> Awaitable[None]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def update(
        self,
        note: Note,
    ) -> Awaitable[None]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def delete(
        self,
        note_id: UUID,
    ) -> Awaitable[None]:
        raise NotImplementedError  # pragma: no cover
