from tests.helpers.builder import Builder

from src.auth.use_cases.inputs import CreateUserInput


class CreateUserInputBuilder(Builder[CreateUserInput]):
    def __init__(self) -> None:
        password = self._faker.password()
        self._data: dict[str, object] = {
            "email": self._faker.email(),
            "password": password,
            "password_confirmation": password,
            "first_name": self._faker.first_name(),
            "last_name": self._faker.last_name(),
        }
        self.initial_data = {**self._data}

    def with_email(self, email: str) -> "CreateUserInputBuilder":
        self._data["email"] = email
        return self

    def with_password(self, password: str) -> "CreateUserInputBuilder":
        self._data["password"] = password
        return self

    def with_password_confirmation(
        self, password_confirmation: str
    ) -> "CreateUserInputBuilder":
        self._data["password_confirmation"] = password_confirmation
        return self

    def with_first_name(self, first_name: str) -> "CreateUserInputBuilder":
        self._data["first_name"] = first_name
        return self

    def with_last_name(self, last_name: str) -> "CreateUserInputBuilder":
        self._data["last_name"] = last_name
        return self

    def build(self) -> CreateUserInput:
        input_ = CreateUserInput.model_validate(self._data)
        self._data = {**self.initial_data}
        return input_

    def build_dict(self) -> dict[str, object]:
        data = self._data
        self._data = {**self.initial_data}
        return data
