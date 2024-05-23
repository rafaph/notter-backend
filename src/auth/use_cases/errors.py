class EmailAlreadyExistsError(Exception):
    def __init__(self, msg: str = "Email already exists") -> None:
        super().__init__(msg)


class InvalidCredentialsError(Exception):
    def __init__(self, msg: str = "Invalid credentials") -> None:
        super().__init__(msg)


class InvalidTokenError(Exception):
    def __init__(self, msg: str = "Invalid token") -> None:
        super().__init__(msg)
