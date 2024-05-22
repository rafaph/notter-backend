import datetime

from src.auth.ports.jwt_manager import JwtManager, TokenPayload
from src.auth.ports.password_hasher import PasswordHasher
from src.auth.ports.repositories.user_repository import UserRepository
from src.auth.use_cases.errors import InvalidCredentialsError
from src.auth.use_cases.inputs import AuthenticateInput
from src.auth.use_cases.output import AuthenticateOutput
from src.common.settings import settings


class AuthenticateUseCase:
    def __init__(
        self,
        repository: UserRepository,
        jwt_manager: JwtManager,
        password_hasher: PasswordHasher,
    ) -> None:
        self._repository = repository
        self._jwt_manager = jwt_manager
        self._password_hasher = password_hasher

    async def __call__(self, data: AuthenticateInput) -> AuthenticateOutput:
        user = await self._repository.find_by_email(data.email)

        if user is None:
            raise InvalidCredentialsError()

        if not self._password_hasher.verify(user.password, data.password):
            raise InvalidCredentialsError()

        now = datetime.datetime.now(datetime.UTC).replace(microsecond=0)
        exp = now + datetime.timedelta(
            minutes=settings.EXPIRATION_TIME_MINUTES,
        )
        token_payload = TokenPayload(
            sub=user.id,
            exp=exp,
            nbf=now,
            iat=now,
        )
        access_token = self._jwt_manager.encode(token_payload)

        return AuthenticateOutput(
            access_token=access_token,
            token_type="Bearer",  # noqa: S106
        )
