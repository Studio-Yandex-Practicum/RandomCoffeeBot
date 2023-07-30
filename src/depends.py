from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .settings import Settings

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"


class Container(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)
    engine = providers.Singleton(create_async_engine, DATABASE_URL, future=True, echo=True)
    sessionmaker = providers.Singleton(async_sessionmaker, engine, expire_on_commmit=False)
