from src.core.db.models import User
from src.core.db.repository.base import AbstractRepository


class UserRepository(AbstractRepository(User)):  # type: ignore[misc]
    _model = User
