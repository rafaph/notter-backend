from typing import Self

from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema

from src.auth.domain.entities.user import User


class CreateUserOutput(User):
    password: SkipJsonSchema[str] = Field(default="none", exclude=True)

    @classmethod
    def from_user(cls, user: User) -> Self:
        return cls(**user.model_dump(exclude={"password"}))


class AuthenticateOutput(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class GetProfileOutput(CreateUserOutput): ...


class UpdateUserOutput(CreateUserOutput): ...
