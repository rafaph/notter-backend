from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from tests.helpers.builder import Builder

from src.auth.ports.jwt_manager import TokenPayload


class TokenPayloadBuilder(Builder[TokenPayload]):
    def __init__(self) -> None:
        now = datetime.now(UTC).replace(microsecond=0)
        self._data = {
            "sub": uuid4(),
            "exp": now + timedelta(minutes=15),
            "nbf": now,
            "iat": now,
        }

    def with_sub(self, sub: UUID) -> "TokenPayloadBuilder":
        self._data["sub"] = sub
        return self

    def with_exp(self, exp: datetime) -> "TokenPayloadBuilder":
        self._data["exp"] = exp.replace(microsecond=0)
        return self

    def with_nbf(self, nbf: datetime) -> "TokenPayloadBuilder":
        self._data["nbf"] = nbf.replace(microsecond=0)
        return self

    def with_iat(self, iat: datetime) -> "TokenPayloadBuilder":
        self._data["iat"] = iat.replace(microsecond=0)
        return self

    def build(self) -> TokenPayload:
        return TokenPayload.model_validate(self._data)
