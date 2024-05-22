from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    @abstractmethod
    def verify(self, hash_: str, password: str) -> bool:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def hash(self, password: str) -> str:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def needs_rehash(self, hash_: str) -> bool:
        raise NotImplementedError  # pragma: no cover
