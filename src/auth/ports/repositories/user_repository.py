from abc import ABC, abstractmethod
from collections.abc import Awaitable
from uuid import UUID

from src.auth.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> Awaitable[None]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def find_by_email(self, email: str) -> Awaitable[User | None]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def find_by_id(self, user_id: UUID) -> Awaitable[User | None]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def update(self, user: User) -> Awaitable[None]:
        raise NotImplementedError  # pragma: no cover
