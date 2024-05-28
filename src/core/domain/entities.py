from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.common.datetime import Datetime


class Category(BaseModel):
    id: UUID = Field(strict=True, default_factory=uuid4)
    user_id: UUID = Field(strict=True)
    name: str = Field(strict=True, min_length=1, max_length=255)
    created_at: datetime = Field(
        strict=True,
        default_factory=Datetime.now,
    )
    updated_at: datetime = Field(
        strict=True,
        default_factory=Datetime.now,
    )


class Note(BaseModel):
    id: UUID = Field(strict=True, default_factory=uuid4)
    user_id: UUID = Field(strict=True)
    title: str = Field(strict=True, min_length=1, max_length=255)
    content: str = Field(strict=True, min_length=1)
    created_at: datetime = Field(
        strict=True,
        default_factory=Datetime.now,
    )
    updated_at: datetime = Field(
        strict=True,
        default_factory=Datetime.now,
    )


class NoteCategory(BaseModel):
    note_id: UUID = Field(strict=True)
    category_id: UUID = Field(strict=True)
    created_at: datetime = Field(
        strict=True,
        default_factory=Datetime.now,
    )
    updated_at: datetime = Field(
        strict=True,
        default_factory=Datetime.now,
    )
