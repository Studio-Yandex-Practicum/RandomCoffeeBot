from sqlalchemy import select

from src.core.db.models import User
from src.core.db.repository.base import AbstractRepository


class UserRepository(AbstractRepository[User]):
    _model = User

    async def get_by_username(self, username: str) -> User | None:
        async with self._sessionmaker() as session:
            instance = await session.scalar(select(self._model).where(self._model.username == username))
            return instance

    async def create_or_update(self, instance: User) -> User | None:
        """Создаёт нового или обновляет существующего пользователя в базе данных."""
        db_instance = await self.get_by_username(instance.username)
        if db_instance is None:
            return await self.create(instance)
        return await self.update(instance.id, db_instance)

    async def get_by_status(self, status: str) -> list[User] | None:
        """Получает пользователей по статусу участия во встречах."""
        async with self._sessionmaker() as session:
            return await session.scalars(select(self._model).where(self._model.status == status))
