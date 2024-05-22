from src.common.adapters.errors import ExternalError


class HashingError(ExternalError):
    def __init__(self, error: Exception) -> None:
        self.error = error

    def __str__(self) -> str:
        return str(self.error)
