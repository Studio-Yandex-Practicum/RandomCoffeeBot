from sqlalchemy import and_, select

from src.core.db.models import StatusEnum, User
from src.core.db.repository.base import AbstractRepository
from src.core.exceptions.exceptions import NoUserFoundError


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

    async def get_free_user(self) -> User | None:
        """Получает пользователя ожидающего встречи."""
        async with self._sessionmaker() as session:
            return await session.scalar(select(self._model).where(self._model.status == StatusEnum.WAITING_MEETING))

    async def get_without_current(self, user: User) -> User:
        """Возвращает пользователя со статусом ожидания встречи, исключая текущего пользователя."""
        async with self._sessionmaker() as session:
            if user_current := await session.scalar(
                select(self._model).where(
                    and_(self._model.id != user.id, self._model.status == StatusEnum.WAITING_MEETING)
                )
            ):
                return user_current
            raise NoUserFoundError(user.id)
