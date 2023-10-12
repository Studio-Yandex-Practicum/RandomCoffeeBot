from src.core.db.models import MatchStatusEnum, StatusEnum, User, UsersMatch
from src.core.db.repository.base import AbstractRepository
from src.core.db.repository.user import UserRepository


class UsersMatchRepository(AbstractRepository[UsersMatch]):
    _model = UsersMatch

    async def create_matching(self, _user_repository: UserRepository) -> None:
        """Создаёт метчи для участников встреч."""
        # Необходима проверка уникальных пар
        waiting_meetings: list[User] = iter(await _user_repository.get_by_status(
            StatusEnum.WAITING_MEETING
        ))
        matches: list[UsersMatch] = []
        need_updating: list[dict[User, User]] = []
        for user_one, user_two in zip(waiting_meetings, waiting_meetings):
            matches.append(
                UsersMatch(
                    matched_user_one=user_one.id,
                    matched_user_two=user_two.id,
                    status=MatchStatusEnum.ONGOING
                )
            )
            for user in (user_one, user_two):
                need_updating.append(
                    {'id': user.id, 'status': StatusEnum.IN_MEETING}
                )
        await self.create_all(matches)
        await _user_repository.update_all(need_updating)
