from pydantic import BaseModel, EmailStr, Field, model_validator

from src.auth.domain.entities.user import User
from src.auth.ports.password_hasher import PasswordHasher


class CreateUserInput(BaseModel):
    email: EmailStr
    password: str = Field(strict=True, min_length=1)
    password_confirmation: str = Field(strict=True, min_length=1)
    first_name: str = Field(strict=True, min_length=1)
    last_name: str = Field(strict=True, min_length=1)

    @model_validator(mode="after")
    def _passwords_validator(self) -> "CreateUserInput":
        if self.password != self.password_confirmation:
            msg = "passwords do not match"
            raise ValueError(msg)
        return self

    def to_user(self, password_hasher: PasswordHasher) -> User:
        return User(
            email=self.email,
            password=password_hasher.hash(self.password),
            first_name=self.first_name,
            last_name=self.last_name,
        )
