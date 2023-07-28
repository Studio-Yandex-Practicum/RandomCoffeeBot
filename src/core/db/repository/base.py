import abc
from typing import Generic, TypeVar

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core import exceptions

Model = TypeVar("Model")


class AbstractRepository(abc.ABC, Generic[Model]):
    """Абстрактный класс, для реализации паттерна Repository."""

    _model: type[Model]

    def __init__(self, sessionmaker: sessionmaker[AsyncSession]) -> None:
        self._sessionmaker = sessionmaker

    async def get_or_none(self, instance_id: int) -> Model | None:
        """Получает из базы объект модели по ID. В случае отсутствия возвращает None."""
        instance = await self._sessionmaker.execute(select(self._model).where(self._model.id == instance_id))
        return instance.scalars().first()

    async def get(self, instance_id: int) -> Model:
        """Получает объект модели по ID. В случае отсутствия объекта бросает ошибку."""
        db_obj = await self.get_or_none(instance_id)
        if db_obj is None:
            raise exceptions.ObjectNotFoundError(self._model, instance_id)
        return db_obj

    async def create(self, instance: Model) -> Model:
        """Создает новый объект модели и сохраняет в базе."""
        self._sessionmaker.add(instance)
        try:
            await self._sessionmaker.commit()
        except IntegrityError:
            raise exceptions.ObjectAlreadyExistsError(instance)

        await self._sessionmaker.refresh(instance)
        return instance

    async def update(self, instance_id: int, instance: Model) -> Model:
        """Обновляет существующий объект модели в базе."""
        instance.id = instance_id
        instance = await self._sessionmaker.merge(instance)
        await self._sessionmaker.commit()
        return instance  # noqa: R504

    async def update_all(self, instances: list[dict]) -> list[Model]:
        """Обновляет несколько измененных объектов модели в базе."""
        update_objects = await self._sessionmaker.execute(update(self._model), instances)
        await self._sessionmaker.commit()
        return update_objects

    async def get_all(self) -> list[Model]:
        """Возвращает все объекты модели из базы данных."""
        objects = await self._sessionmaker.execute(select(self._model))
        return objects.scalars().all()

    async def create_all(self, objects: list[Model]) -> None:
        """Создает несколько объектов модели в базе данных."""
        self._sessionmaker.add_all(objects)
