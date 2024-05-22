from abc import ABC, abstractmethod
from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, PlainSerializer


class TokenPayload(BaseModel):
    sub: Annotated[
        UUID,
        PlainSerializer(
            lambda v: str(v),
            return_type=str,
            when_used="unless-none",
        ),
    ]
    exp: datetime
    nbf: datetime
    iat: datetime


class JwtManager(ABC):
    @abstractmethod
    def encode(self, payload: TokenPayload) -> str:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def decode(self, token: str) -> TokenPayload:
        raise NotImplementedError  # pragma: no cover
