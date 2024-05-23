import os

from pydantic import BaseModel, PostgresDsn, ValidationError


class InvalidSettingsError(Exception):
    def __init__(self, msg: str = "Invalid settings") -> None:
        super().__init__(msg)


class BaseSettings:
    DATABASE_URL: PostgresDsn
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRATION_TIME_MINUTES: int


class Settings(BaseSettings, BaseModel): ...


class LazySettings(BaseSettings):
    def __init__(self) -> None:
        self._settings: Settings | None = None

    def _initialize(self) -> None:
        try:
            self._settings = Settings.model_validate(os.environ)
        except ValidationError as error:
            raise InvalidSettingsError() from error

    def __getattr__(self, name: str) -> object:
        if self._settings is None:
            self._initialize()
        return getattr(self._settings, name)


settings = LazySettings()
