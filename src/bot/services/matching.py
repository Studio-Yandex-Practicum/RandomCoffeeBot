import structlog

from src.core.db.models import StatusEnum, UsersMatch
from src.core.db.repository.user import UserRepository
from src.core.db.repository.usersmatch import UsersMatchRepository

log = structlog.get_logger()


class MatchingService:
    """Сервис представляющий логику подбора пар между пользователями."""

    def __init__(self, user_repository: UserRepository, match_repository: UsersMatchRepository) -> None:
        self._user_repository = user_repository
        self._match_repository = match_repository

    async def run_matching(self) -> list[UsersMatch]:
        """Запускает создание метчей."""
        matches: list[UsersMatch] = []
        while user_one := await self._user_repository.get_free_user():
            if user_two := await self._user_repository.get_without_current(user_one):
                matches.append(match := await self._match_repository.make_match_for_user(user_one, user_two))
                for user in (user_one, user_two):
                    user.status = StatusEnum.IN_MEETING
                    user.matches.append(match)
                    await self._user_repository.update(user.id, user)
            else:
                log.info(f"Невозможно создать пару для пользователя с id {user.id}.")
        return matches
