from pydantic import PostgresDsn, ValidationError
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    SECRET_KEY: str


try:
    settings = Settings()
except ValidationError as error:  # pragma: no cover
    print(error.json(indent=4))
    msg = "Invalid settings"
    raise Exception(msg) from error
