from itertools import combinations

from sqlalchemy import select

from src.core.db.models import MatchStatusEnum, StatusEnum, User, UsersMatch
from src.core.db.repository.base import AbstractRepository


class UsersMatchRepository(AbstractRepository[UsersMatch]):
    _model = UsersMatch
    _user_model = User

    async def waiting_meeting(self, status: str) -> list:
        async with self._sessionmaker() as session:
            instances = await session.execute(select(self._user_model).where(self._user_model.status == status))
            return instances.fetchall()

    async def check_unique_matching(self, user_1: User, user_2: User):
        async with self._sessionmaker() as session:
            instances = await session.execute(
                select(self._model).where(
                    matched_user_one=user_1, matched_user_two=user_2, status=MatchStatusEnum.ONGOING
                )
            ).scalar()
            return instances

    async def matching(self) -> list[UsersMatch]:
        db_instance = await self.waiting_meeting(StatusEnum.WAITING_MEETING)
        combinations_list = combinations(db_instance, 2)
        pairs = []
        async with self._sessionmaker() as session:
            for user1, user2 in combinations_list:
                if self.check_unique_matching(user_1=user1, user_2=user2) is None:
                    new_pair = self._model(
                        matched_user_one=user1, matched_user_two=user2, status=MatchStatusEnum.ONGOING
                    )
                    session.add(new_pair)
                    pairs.append(new_pair)
            return pairs
