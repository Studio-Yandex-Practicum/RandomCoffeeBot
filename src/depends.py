from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.bot.services.admin import AdminService
from src.core.db.repository.admin import AdminRepository
from src.settings import Settings


class Container(containers.DeclarativeContainer):
    # Settings
    settings = providers.Singleton(Settings)
    # DB Connection
    engine = providers.Singleton(create_async_engine, settings.provided.database_url, future=True, echo=True)
    sessionmaker = providers.Singleton(async_sessionmaker, engine, expire_on_commmit=False)
    # Repository
    admin_repository = providers.Factory(AdminRepository, sessionmaker=sessionmaker)
    # Services
    admin_service = providers.Factory(
        AdminService, admin_repository=admin_repository, admin_username=settings.provided.ADMIN_USERNAME
    )
