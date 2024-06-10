from uuid import UUID, uuid4

from tests.helpers.builder import Builder

from src.core.domain.entities import NoteCategory


class NoteCategoryBuilder(Builder[NoteCategory]):
    def __init__(self) -> None:
        self._data = {
            "note_id": uuid4(),
            "category_id": uuid4(),
        }

    def with_note_id(self, note_id: UUID) -> "NoteCategoryBuilder":
        self._data["note_id"] = note_id
        return self

    def with_category_id(self, category_id: UUID) -> "NoteCategoryBuilder":
        self._data["category_id"] = category_id
        return self

    def build(self) -> NoteCategory:
        return NoteCategory.model_validate(self._data)
