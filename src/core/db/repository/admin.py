from sqlalchemy import select

from src.core.db.models import Admin
from src.core.db.repository.base import AbstractRepository
from src.settings import Settings


class AdminRepository(AbstractRepository):
    _model = Admin

    async def get_admin_id(self, settings: Settings) -> int | None:
        async with self._sessionmaker() as session:
            instance = await session.scalar(select(self.user_id).where(self.username == settings.ADMIN))
            return instance
