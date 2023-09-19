from src.core.db.models import User
from src.core.db.repository.usersmatch import UsersMatchRepository


class MatchingService:
    """Сервис представляющий логику нахождения пары."""

    _model = User

    def __init__(self, match_repository: UsersMatchRepository):
        self._match_repository = match_repository

    async def create_pairs(self) -> None:
        await self._match_repository.matching()
