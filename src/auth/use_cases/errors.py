class UserNotFoundError(Exception):
    def __init__(
        self, msg: str = "User not found"
    ) -> None:  # pragma: no cover
        super().__init__(msg)


class EmailAlreadyExistsError(Exception):
    def __init__(self, msg: str = "Email already exists") -> None:
        super().__init__(msg)
