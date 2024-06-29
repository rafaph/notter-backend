class CategoryAlreadyExistsError(Exception):
    def __init__(self, msg: str = "Category already exists") -> None:
        super().__init__(msg)
