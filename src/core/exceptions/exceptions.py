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


class MatchNotFoundError(Exception):
    def __init__(self, user_id: str) -> None:
        self.detail = f"Встреча пользователя с user_id {user_id} не найдена"

    def __str__(self) -> str:
        return self.detail
