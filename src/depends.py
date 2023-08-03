from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .settings import Settings


class Container(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)
    engine = providers.Singleton(create_async_engine, settings.database_url, future=True, echo=True)
    sessionmaker = providers.Singleton(async_sessionmaker, engine, expire_on_commmit=False)
