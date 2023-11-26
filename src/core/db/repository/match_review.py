from src.core.db.models import MatchReview, UsersMatch
from src.core.db.repository.base import AbstractRepository


class MatchReviewRepository(AbstractRepository[MatchReview]):
    _model = MatchReview

    async def set_match_review_answer(self, match: UsersMatch, user_id: str, answer: str):
        if user_id == match.object_user_one.user_id:
            user = match.object_user_one
        elif user_id == match.object_user_two.user_id:
            user = match.object_user_two
        return await self.create(MatchReview(usersmatch_id=match.id, user_id=user.id, user_answer=answer))
