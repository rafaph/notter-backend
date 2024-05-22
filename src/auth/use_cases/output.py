from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema

from src.auth.domain.entities.user import User


class CreateUserOutput(User):
    password: SkipJsonSchema[str] = Field(default="none", exclude=True)

    @staticmethod
    def from_user(user: User) -> "CreateUserOutput":
        return CreateUserOutput(**user.model_dump(exclude={"password"}))


class AuthenticateOutput(BaseModel):
    access_token: str
    token_type: str = "Bearer"
