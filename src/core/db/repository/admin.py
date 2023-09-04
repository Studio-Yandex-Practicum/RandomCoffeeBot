from sqlalchemy import select

from src.core.db.models import Admin
from src.core.db.repository.base import AbstractRepository


class AdminRepository(AbstractRepository[Admin]):
    _model = Admin

    async def get_by_user_id(self, user_id: int) -> Admin | None:
        instance = await self._session.scalar(select(self._model).where(self._model.user_id == user_id))
        return instance
