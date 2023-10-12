from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.bot.services.admin import AdminService
from src.bot.services.matching import MatchingService
from src.bot.services.registration import RegistrationService
from src.core.db.repository.admin import AdminRepository
from src.core.db.repository.user import UserRepository
from src.core.db.repository.usersmatch import UsersMatchRepository
from src.settings import Settings


class Container(containers.DeclarativeContainer):
    # Settings
    settings = providers.Singleton(Settings)
    # DB Connection
    engine = providers.Singleton(create_async_engine, settings.provided.database_url, future=True, echo=True)
    sessionmaker = providers.Singleton(async_sessionmaker, engine, expire_on_commit=False)
    # Repository
    admin_repository = providers.Factory(AdminRepository, sessionmaker=sessionmaker)
    user_repository = providers.Factory(UserRepository, sessionmaker=sessionmaker)
    match_repository = providers.Factory(UsersMatchRepository, sessionmaker=sessionmaker)
    # Services
    admin_service = providers.Factory(
        AdminService, admin_repository=admin_repository, admin_username=settings.provided.ADMIN_USERNAME
    )
    registration_service = providers.Factory(RegistrationService, user_repository=user_repository)
    matching_service = providers.Factory(MatchingService, user_repository=user_repository, match_repository=match_repository)
