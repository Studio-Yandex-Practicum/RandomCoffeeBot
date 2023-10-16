from src.core.db.models import StatusEnum, UsersMatch
from src.core.db.repository.user import UserRepository
from src.core.db.repository.usersmatch import UsersMatchRepository


class MatchingService:
    """Сервис представляющий логику подбора пар между пользователями."""

    def __init__(self, user_repository: UserRepository, match_repository: UsersMatchRepository) -> None:
        self._user_repository = user_repository
        self._match_repository = match_repository

    async def set_in_meeting_status(self, user_id: int) -> None:
        """Устанавливает статус in_meeting для встречи после опроса."""
        current_user = await self._user_repository.get(instance_id=user_id)
        current_user.status = StatusEnum.IN_MEETING
        await self._user_repository.update(user_id, current_user)

    async def run_matching(self) -> list[UsersMatch]:
        """Запускает создание метчей."""
        matches: list[UsersMatch] = []
        while user := await self._user_repository.get_free_user():
            matches.append(await self._match_repository.make_match_for_user(user, self._user_repository))
        return matches
