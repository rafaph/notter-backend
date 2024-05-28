from uuid import UUID, uuid4

from tests.helpers.builder import Builder

from src.core.domain.entities import Note


class NoteBuilder(Builder[Note]):
    def __init__(self) -> None:
        self._data = {
            "user_id": uuid4(),
            "title": self._faker.catch_phrase(),
            "content": self._faker.paragraph(),
        }

    def with_id(self, id_: UUID) -> "NoteBuilder":
        self._data["id"] = id_
        return self

    def with_user_id(self, user_id: UUID) -> "NoteBuilder":
        self._data["user_id"] = user_id
        return self

    def build(self) -> Note:
        return Note.model_validate(self._data)
