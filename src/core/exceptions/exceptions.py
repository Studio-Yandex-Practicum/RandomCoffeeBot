from src.core.db.models import Base as DatabaseModel


class ObjectNotFoundError(Exception):
    def __init__(self, model: DatabaseModel, object_id: int) -> None:
        self.detail = f"Объект '{model.__name__}' с id '{object_id}' не найден."

    def __str__(self) -> str:
        return self.detail


class ObjectAlreadyExistsError(Exception):
    def __init__(self, obj: DatabaseModel) -> None:
        self.detail = f"Объект {obj} уже существует"

    def __str__(self) -> str:
        return self.detail


class NoUserFoundError(Exception):
    def __init__(self, object_id: int) -> None:
        self.detail = f"Невозможно создать пару для пользователя с id {object_id}."

    def __str__(self) -> str:
        return self.detail
