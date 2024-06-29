from uuid import UUID

from pydantic import BaseModel, Field

from src.core.domain.entities import Category


class CreateCategoryInputBase(BaseModel):
    name: str = Field(
        strict=True,
        min_length=1,
        max_length=255,
    )


class CreateCategoryInput(CreateCategoryInputBase):
    user_id: UUID = Field(strict=True)

    def to_category(self) -> Category:
        return Category(
            user_id=self.user_id,
            name=self.name,
        )
