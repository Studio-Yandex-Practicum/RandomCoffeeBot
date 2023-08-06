from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.db.repository.user import UserRepository
from settings import Settings
from src.bot.services.registration import RegistrationService


class Container(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)
    engine = providers.Singleton(create_async_engine, settings.provided.database_url, future=True, echo=True)
    sessionmaker = providers.Singleton(async_sessionmaker, engine, expire_on_commmit=False)
    user_repository = providers.Factory(UserRepository, sessionmaker=sessionmaker)
    registration_service = providers.Factory(RegistrationService, user_respository=user_repository)
