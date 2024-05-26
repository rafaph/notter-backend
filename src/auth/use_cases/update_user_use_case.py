from uuid import UUID

from src.auth.domain.entities import User
from src.auth.ports.password_hasher import PasswordHasher
from src.auth.ports.repositories.user_repository import UserRepository
from src.auth.use_cases.errors import EmailAlreadyExistsError
from src.auth.use_cases.inputs import UpdateUserInput
from src.auth.use_cases.output import UpdateUserOutput


class UpdateUserUseCase:
    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._repository = repository
        self._password_hasher = password_hasher

    async def _email_in_use(
        self,
        user_id: UUID,
        email: str | None,
    ) -> bool:
        if email is None:
            return False

        user = await self._repository.find_by_email(email)
        if user is None:
            return False

        return user.id != user_id

    async def __call__(
        self,
        current_user: User,
        data: UpdateUserInput,
    ) -> UpdateUserOutput:
        if await self._email_in_use(current_user.id, data.email):
            raise EmailAlreadyExistsError()

        updated_user = data.to_user(current_user, self._password_hasher)
        await self._repository.update(updated_user)

        return UpdateUserOutput.from_user(updated_user)
