from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Generic, TypeVar

from faker import Faker

T = TypeVar("T")


class Builder(ABC, Generic[T]):
    _faker = Faker("en_US")

    @abstractmethod
    def build(self) -> T:
        raise NotImplementedError

    def build_many(self, number: int | None = None) -> Sequence[T]:
        if number is None:
            number = self._faker.random_int(2, 10)

        return [self.build() for _ in range(number)]
