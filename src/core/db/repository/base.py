import abc
from typing import Generic, TypeVar

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.db.models import Base
from src.core.exceptions import exceptions

Model = TypeVar("Model", bound=Base)


class AbstractRepository(abc.ABC, Generic[Model]):
    """Абстрактный класс, для реализации паттерна Repository."""

    _model: type[Model]

    def __init__(self, sessionmaker: sessionmaker[AsyncSession]) -> None:
        self._sessionmaker = sessionmaker

    async def get_or_none(self, instance_id: int) -> Model | None:
        """Получает из базы объект модели по ID. В случае отсутствия возвращает None."""
        async with self._sessionmaker() as session:
            instance = await session.scalar(select(self._model).where(self._model.id == instance_id))
        return instance

    async def get(self, instance_id: int) -> Model:
        """Получает объект модели по ID. В случае отсутствия объекта бросает ошибку."""
        db_obj = await self.get_or_none(instance_id)
        if db_obj is None:
            raise exceptions.ObjectNotFoundError(self._model.Base, instance_id)
        return db_obj

    async def create(self, instance: Model) -> Model:
        """Создает новый объект модели и сохраняет в базе."""
        async with self._sessionmaker() as session:
            session.add(instance)
            try:
                await session.commit()
            except IntegrityError:
                raise exceptions.ObjectAlreadyExistsError(instance)
            await session.refresh(instance)
        return instance

    async def update(self, instance_id: int, instance: Model) -> Model:
        """Обновляет существующий объект модели в базе."""
        async with self._sessionmaker() as session:
            instance.id = instance_id
            instance = await session.merge(instance)
            await session.commit()
        return instance

    async def update_all(self, instances: list[dict[Model, Model]]) -> list[dict[Model, Model]]:
        """Обновляет несколько измененных объектов модели в базе."""
        async with self._sessionmaker() as session:
            await session.execute(update(self._model), instances)
            await session.commit()
        return instances

    async def get_all(self) -> list[Model]:
        """Возвращает все объекты модели из базы данных."""
        async with self._sessionmaker() as session:
            objects = await session.scalars(select(self._model))
        return objects

    async def create_all(self, instances: list[Model]) -> None:
        """Создает несколько объектов модели в базе данных."""
        async with self._sessionmaker() as session:
            session.add_all(instances)
            await session.commit()
