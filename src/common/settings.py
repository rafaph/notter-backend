import logging
import os
import sys
from enum import Enum
from typing import cast

from pydantic import BaseModel, PostgresDsn, ValidationError, computed_field

logger = logging.getLogger(__name__)


class EnvEnum(str, Enum):
    dev = "dev"
    prod = "prod"
    test = "test"


class Settings(BaseModel):
    DATABASE_URL: PostgresDsn
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_TIME_MINUTES: int
    SERVER_HOST: str
    SERVER_PORT: int
    SERVER_RELOAD: bool = False
    SERVER_WORKERS: int | None = None
    SERVER_ROOT_PATH: str = ""
    SERVER_PROXY_HEADERS: bool = False
    ENV: EnvEnum

    @computed_field  # type: ignore[misc]
    @property
    def testing(self) -> bool:
        return EnvEnum.test == self.ENV


class LazySettings:
    def __init__(self) -> None:
        self._settings: Settings | None = None

    def _initialize(self) -> None:
        try:
            self._settings = Settings.model_validate(os.environ)
        except ValidationError as error:
            logger.error(
                msg="Invalid settings",
                extra={"errors": error.errors(include_input=False)},
            )
            sys.exit(1)

    def __getattr__(self, name: str) -> object:
        if self._settings is None:
            self._initialize()
        return getattr(self._settings, name)


settings = cast(Settings, LazySettings())
