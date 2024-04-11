from sqlalchemy import select

from src.core.db.models import MatchReview, UsersMatch
from src.core.db.repository.base import AbstractRepository
from src.core.exceptions.exceptions import ObjectAlreadyExistsError


class MatchReviewRepository(AbstractRepository[MatchReview]):
    _model = MatchReview

    async def set_match_review_answer(self, match: UsersMatch, user_id: str, answer: str) -> MatchReview:
        if user_id == match.object_user_one.user_id:
            user = match.object_user_one
        elif user_id == match.object_user_two.user_id:
            user = match.object_user_two
        if await self.get_match_review_if_already_exists(usersmatch_id=match.id, user_id=user.id):
            raise ObjectAlreadyExistsError(self._model)  # type: ignore[arg-type]
        return await self.create(MatchReview(usersmatch_id=match.id, user_id=user.id, user_answer=answer))

    async def get_match_review_if_already_exists(
        self,
        usersmatch_id: int,
        user_id: int,
    ) -> MatchReview | None:
        async with self._sessionmaker() as session:
            match_review = await session.scalar(
                select(self._model).where(
                    (self._model.usersmatch_id == usersmatch_id) & (self._model.user_id == user_id)
                )
            )
        return match_review
