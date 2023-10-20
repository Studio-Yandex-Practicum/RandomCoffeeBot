from sqlalchemy import and_, or_, select

from src.core.db.models import MatchStatusEnum, User, UsersMatch
from src.core.db.repository.base import AbstractRepository
from src.core.exceptions.exceptions import ObjectAlreadyExistsError


class UsersMatchRepository(AbstractRepository[UsersMatch]):
    _model = UsersMatch

    async def make_match_for_user(self, user_one: User, user_two: User) -> UsersMatch:
        """Создаёт метчи для участников встреч."""
        await self.check_unique_matching(user_one, user_two)
        return await self.create(
            UsersMatch(matched_user_one=user_one.id, matched_user_two=user_two.id, status=MatchStatusEnum.ONGOING)
        )

    async def check_unique_matching(self, user_one: User, user_two: User):
        async with self._sessionmaker() as session:
            if match := await session.scalar(
                select(self._model)
                .where(
                    or_(
                        and_(
                            self._model.matched_user_one == user_one.id,
                            self._model.matched_user_two == user_two.id,
                        ),
                        and_(
                            self._model.matched_user_one == user_two.id,
                            self._model.matched_user_two == user_one.id,
                        ),
                    )
                )
                .filter(
                    self._model.status == MatchStatusEnum.ONGOING,
                )
            ):
                raise ObjectAlreadyExistsError(match)
