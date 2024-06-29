from typing import Self
from uuid import UUID

from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from src.core.domain.entities import Category


class CreateCategoryOutput(Category):
    user_id: SkipJsonSchema[UUID] = Field(exclude=True)

    @classmethod
    def from_category(cls, category: Category) -> Self:
        return cls(**category.model_dump())
