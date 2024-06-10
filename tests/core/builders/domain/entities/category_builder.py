from uuid import UUID, uuid4

from tests.helpers.builder import Builder

from src.core.domain.entities import Category


class CategoryBuilder(Builder[Category]):
    def __init__(self) -> None:
        self._data = {
            "user_id": uuid4(),
            "name": self._faker.first_name(),
        }

    def with_id(self, id_: UUID) -> "CategoryBuilder":
        self._data["id"] = id_
        return self

    def with_user_id(self, user_id: UUID) -> "CategoryBuilder":
        self._data["user_id"] = user_id
        return self

    def with_name(self, name: str) -> "CategoryBuilder":
        self._data["name"] = name
        return self

    def build(self) -> Category:
        return Category.model_validate(self._data)
