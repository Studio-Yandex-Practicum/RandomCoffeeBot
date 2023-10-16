from sqlalchemy import select

from src.core.db.models import MatchStatusEnum, StatusEnum, User, UsersMatch
from src.core.db.repository.base import AbstractRepository
from src.core.db.repository.user import UserRepository
from src.core.exceptions.exceptions import ObjectAlreadyExistsError


class UsersMatchRepository(AbstractRepository[UsersMatch]):
    _model = UsersMatch

    async def make_match_for_user(self, user_one: User, user_repository: UserRepository) -> UsersMatch:
        """Создаёт метчи для участников встреч."""
        user_two = await user_repository.get_without_current(user_one)
        await self.check_unique_matching(user_one, user_two)
        for user in (user_one, user_two):
            user.status = StatusEnum.IN_MEETING
            await user_repository.update(user.id, user)
        return await self.create(
            UsersMatch(matched_user_one=user_one.id, matched_user_two=user_two.id, status=MatchStatusEnum.ONGOING)
        )

    async def check_unique_matching(self, user_one: User, user_two: User):
        async with self._sessionmaker() as session:
            if match := await session.scalar(
                select(self._model).where(
                    self._model.matched_user_one == user_one.id,
                    self._model.matched_user_two == user_two.id,
                    self._model.status == MatchStatusEnum.ONGOING,
                )
            ):
                raise ObjectAlreadyExistsError(match)
