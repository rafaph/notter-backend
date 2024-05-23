from src.auth.domain.entities.user import User
from src.auth.ports.jwt_manager import JwtManager
from src.auth.ports.repositories.user_repository import UserRepository
from src.auth.use_cases.errors import (
    InvalidTokenError,
)


class GetUserFromTokenUseCase:
    def __init__(
        self,
        repository: UserRepository,
        jwt_manager: JwtManager,
    ) -> None:
        self._repository = repository
        self._jwt_manager = jwt_manager

    async def __call__(self, token: str) -> User:
        payload = self._jwt_manager.decode(token)
        if payload is None:
            raise InvalidTokenError()

        user = await self._repository.find_by_id(payload.sub)
        if user is None:
            raise InvalidTokenError()

        return user
