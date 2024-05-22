from datetime import datetime
from uuid import UUID

from tests.helpers.builder import Builder

from src.auth.domain.entities.user import User


class UserBuilder(Builder[User]):
    def __init__(self) -> None:
        self._data: dict[str, object] = {
            "email": self._faker.email(),
            "password": self._faker.password(),
            "first_name": self._faker.first_name(),
            "last_name": self._faker.last_name(),
        }

    def with_id(self, id_: UUID | str) -> "UserBuilder":
        if isinstance(id_, str):
            id_ = UUID(id_)
        self._data["id"] = id_
        return self

    def with_email(self, email: str) -> "UserBuilder":
        self._data["email"] = email
        return self

    def with_password(self, password: str) -> "UserBuilder":
        self._data["password"] = password
        return self

    def with_first_name(self, first_name: str) -> "UserBuilder":
        self._data["first_name"] = first_name
        return self

    def with_last_name(self, last_name: str) -> "UserBuilder":
        self._data["last_name"] = last_name
        return self

    def with_updated_at(self, updated_at: datetime) -> "UserBuilder":
        self._data["updated_at"] = updated_at
        return self

    def with_created_at(self, created_at: datetime) -> "UserBuilder":
        self._data["created_at"] = created_at
        return self

    def build(self) -> User:
        return User.model_validate(self._data)
