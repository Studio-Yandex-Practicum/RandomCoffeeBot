from src.core.db.models import StatusEnum
from src.core.db.repository.user import UserRepository
from src.core.db.repository.usersmatch import UsersMatchRepository


class MatchingService:
    """Сервис представляющий логику подбора пар между пользователями."""

    def __init__(
        self,
        user_repository: UserRepository,
        match_repository: UsersMatchRepository
    ) -> None:
        self._user_repository = user_repository
        self._match_repository = match_repository

    async def set_waiting_status(self, user_id: int) -> None:
        """Устанавливает статус ождидания встречи после опроса."""
        current_user = await self._user_repository.get(instance_id=user_id)
        current_user.status = StatusEnum.IN_MEETING
        await self._user_repository.update(user_id, current_user)

    async def run_matching(self) -> None:
        """Запускает создание метчей."""
        await self._match_repository.create_matching(self._user_repository)
