import datetime
import secrets
from uuid import UUID

import jwt


def generate_token(
    user_id: UUID,
    *,
    secret_key: str | None = None,
    algorithm: str = "HS512",
    expiration_time_minutes: int = 10,
) -> str:
    if secret_key is None:
        secret_key = secrets.token_hex(64)
    now = datetime.datetime.now(datetime.UTC).replace(microsecond=0)
    exp = now + datetime.timedelta(
        minutes=expiration_time_minutes,
    )
    claims = {
        "sub": str(user_id),
        "exp": exp,
        "nbf": now,
        "iat": now,
    }
    return jwt.encode(
        claims,
        key=secret_key,
        algorithm=algorithm,
    )
