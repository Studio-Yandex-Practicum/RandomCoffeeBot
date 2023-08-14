from sqlalchemy import select

from src.core.db.models import Admin
from src.core.db.repository.base import AbstractRepository


class AdminRepository(AbstractRepository):
    _model = Admin

    async def get_by_username(self, username: str) -> Admin | None:
        async with self._sessionmaker() as session:
            instance = await session.scalar(select(self._model).where(self.username == username))
            return instance

    async def create_or_update(self, instance: Admin) -> Admin:
        """Создаёт нового или обновляет существующего пользователя в базе данных."""
        db_instance = await self.get_by_username(instance.username)
        if instance:
            return self.update(instance.id, db_instance)
        return self.create(instance)
