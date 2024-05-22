from src.auth.ports.password_hasher import PasswordHasher
from src.auth.ports.repositories.user_repository import UserRepository
from src.auth.use_cases.errors import EmailAlreadyExistsError
from src.auth.use_cases.inputs import CreateUserInput
from src.auth.use_cases.output import CreateUserOutput


class CreateUserUseCase:
    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._repository = repository
        self._password_hasher = password_hasher

    async def _email_in_use(self, email: str) -> bool:
        return await self._repository.find_by_email(email) is not None

    async def __call__(self, data: CreateUserInput) -> CreateUserOutput:
        if await self._email_in_use(data.email):
            raise EmailAlreadyExistsError()

        user = data.to_user(self._password_hasher)

        await self._repository.create(user)

        return CreateUserOutput.from_user(user)
