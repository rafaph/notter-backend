import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC).replace(microsecond=0)


class User(BaseModel):
    id: UUID = Field(strict=True, default_factory=uuid4)
    email: EmailStr
    password: str = Field(strict=True, min_length=1)
    first_name: str = Field(strict=True, min_length=1)
    last_name: str = Field(strict=True, min_length=1)
    updated_at: datetime.datetime = Field(strict=True, default_factory=_now)
    created_at: datetime.datetime = Field(strict=True, default_factory=_now)
