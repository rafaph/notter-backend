import jwt

from src.auth.ports.jwt_manager import JwtManager, TokenPayload


class PyJwtManager(JwtManager):
    def __init__(self, secret_key: str, algorithm: str) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm

    def encode(self, payload: TokenPayload) -> str:
        claims = payload.model_dump(exclude_none=True)
        return jwt.encode(
            claims,
            key=self._secret_key,
            algorithm=self._algorithm,
        )

    def decode(self, token: str) -> TokenPayload | None:
        try:
            payload = jwt.decode(
                token,
                key=self._secret_key,
                algorithms=[self._algorithm],
            )
        except jwt.exceptions.PyJWTError:
            return None

        return TokenPayload.model_validate(payload)
