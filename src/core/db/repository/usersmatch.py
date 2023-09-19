from itertools import combinations

from sqlalchemy import select

from src.core.db.models import MatchStatusEnum, StatusEnum, UsersMatch
from src.core.db.repository.base import AbstractRepository


class UsersMatchRepository(AbstractRepository[UsersMatch]):
    _model = UsersMatch

    async def waiting_meeting(self, status: str) -> list:
        async with self._sessionmaker() as session:
            instances = await session.execute(select(self._model).where(self._model.status == status))
            return instances.fetchall()

    async def matching(self) -> None:
        db_instance = await self.waiting_meeting(StatusEnum.WAITING_MEETING)
        combinations_list = combinations(db_instance, 2)
        for user1, user2 in combinations_list:
            result = self._model(matched_user_one=user1, matched_user_two=user2, status=MatchStatusEnum.ONGOING)
            await self.create(result)
