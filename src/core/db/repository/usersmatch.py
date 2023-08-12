from src.core.db.models import UsersMatch
from src.core.db.repository.base import AbstractRepository


class UsersMatchRepository(AbstractRepository[UsersMatch]):
    _model = UsersMatch
