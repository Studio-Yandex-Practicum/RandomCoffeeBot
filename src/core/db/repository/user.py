from typing import Sequence

from sqlalchemy import ScalarResult, select
from sqlalchemy.orm import joinedload

from src.core.db.models import MatchStatusEnum, StatusEnum, User, UsersMatch
from src.core.db.repository.base import AbstractRepository


class UserRepository(AbstractRepository[User]):
    _model = User

    async def get_all_chat_id(self) -> Sequence[str] | None:
        """Получает все user id для маттермост"""
        async with self._sessionmaker() as session:
            instance = await session.execute(select(self._model.user_id))
            return instance.scalars().all()

    async def get_by_username(self, username: str) -> User | None:
        async with self._sessionmaker() as session:
            instance = await session.scalar(select(self._model).where(self._model.username == username))
            return instance

    async def create_or_update(self, instance: User) -> User | None:
        """Создаёт нового или обновляет существующего пользователя в базе данных."""
        db_instance = await self.get_by_username(instance.username)
        if db_instance is None:
            return await self.create(instance)
        return await self.update(db_instance.id, instance)

    async def get_by_status(self, status: str) -> ScalarResult[User] | None:
        """Получает пользователей по статусу участия во встречах."""
        async with self._sessionmaker() as session:
            users = await session.scalars(select(self._model).where(self._model.status == status))
        return users.all()

    async def get_free_user(self) -> User | None:
        """Получает пользователя ожидающего встречи."""
        async with self._sessionmaker() as session:
            user: User | None = await session.scalar(
                select(self._model)
                .options(joinedload(self._model.matches))
                .where(self._model.status == StatusEnum.WAITING_MEETING)
                .limit(1)
            )
            return user

    async def get_suitable_pair(self, user: User) -> User | None:
        """Возвращает подходящего для встречи пользователя."""
        async with self._sessionmaker() as session:
            pair: User | None = await session.scalar(
                select(self._model)
                .options(joinedload(self._model.matches))
                .where(self._model.id != user.id, self._model.status == StatusEnum.WAITING_MEETING)
                .outerjoin(self._model.matches)
                .where(
                    UsersMatch.id.is_(None)
                    | (UsersMatch.matched_user_one != user.id)
                    | (UsersMatch.matched_user_two != user.id) & (UsersMatch.status != MatchStatusEnum.ONGOING)
                )
                .limit(1)
            )
            return pair

    async def set_in_meeting_status(self, user_id: int) -> None:
        """Устанавливает статус in_meeting для встречи после опроса."""
        current_user = await self.get(instance_id=user_id)
        current_user.status = StatusEnum.IN_MEETING
        await self.update(user_id, current_user)

    async def set_waiting_meeting_status(self, user_id: str) -> None:
        """Устанавливает статус waiting_meeting для встречи после еженедельного опроса."""
        async with self._sessionmaker() as session:
            current_user = await session.scalar(select(self._model).where(self._model.user_id == user_id))
        if current_user is not None:
            current_user.status = StatusEnum.WAITING_MEETING
            await self.update(current_user.id, current_user)
