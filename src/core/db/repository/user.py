from sqlalchemy import or_, select
from sqlalchemy.orm import joinedload

from src.core.db.models import MatchStatusEnum, StatusEnum, User, UsersMatch
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

    async def get_free_user(self) -> User | None:
        """Получает пользователя ожидающего встречи."""
        async with self._sessionmaker() as session:
            return await session.scalar(
                select(self._model)
                .options(joinedload(self._model.matches))
                .where(self._model.status == StatusEnum.WAITING_MEETING)
                .limit(1)
            )

    async def get_without_current(self, user: User) -> User | None:
        """Возвращает пользователя со статусом ожидания встречи, исключая текущего пользователя."""
        async with self._sessionmaker() as session:
            return await session.scalar(
                select(self._model)
                .options(joinedload(self._model.matches))
                .where(self._model.id != user.id, self._model.status == StatusEnum.WAITING_MEETING)
                .join(self._model.matches)
                .filter(
                    or_(UsersMatch.matched_user_one != user.id, UsersMatch.matched_user_two != user.id),
                    UsersMatch.status != MatchStatusEnum.ONGOING,
                )
                .limit(1)
            )

    async def set_in_meeting_status(self, user_id: int) -> None:
        """Устанавливает статус in_meeting для встречи после опроса."""
        current_user = await self.get(instance_id=user_id)
        current_user.status = StatusEnum.IN_MEETING
        await self.update(user_id, current_user)
