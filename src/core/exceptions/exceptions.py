from src.core.db.models import Base as DatabaseModel


class ObjectNotFoundError(Exception):
    def __init__(self, model: DatabaseModel, object_id: int):
        self.detail = f"Объект '{model.__name__}' с id '{object_id}' не найден."

    def __str__(self):
        return self.detail
