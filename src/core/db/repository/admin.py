from sqlalchemy import select

from src.core.db.models import Admin
from src.core.db.repository.base import AbstractRepository


class AdminRepository(AbstractRepository):
    _model = Admin

    async def get_by_user_id(self, user_id: int) -> Admin | None:
        async with self._sessionmaker() as session:
            instance = await session.scalar(select(self._model).where(self._model.user_id == user_id))
            return instance

    async def create(self, instance: Admin) -> Admin:
        return self._create(instance)
