from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import Settings
from src.bot.services.admin import AdminRegistration
from src.core.db.repository.admin import AdminRepository


class Container(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)
    engine = providers.Singleton(create_async_engine, settings.provided.database_url, future=True, echo=True)
    sessionmaker = providers.Singleton(async_sessionmaker, engine, expire_on_commmit=False)
    admin_repository = providers.Factory(AdminRepository, sessionmaker=sessionmaker)
    admin_registration = providers.Factory(AdminRegistration, user_respository=admin_repository)
