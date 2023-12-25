from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.bot.services.admin import AdminService
from src.bot.services.create_message_service import MessageForUsers
from src.bot.services.matching import MatchingService
from src.bot.services.notify_service import NotifyService
from src.bot.services.registration import RegistrationService
from src.core.db.repository.admin import AdminRepository
from src.core.db.repository.match_review import MatchReviewRepository
from src.core.db.repository.user import UserRepository
from src.core.db.repository.usersmatch import UsersMatchRepository
from src.endpoints import Endpoints
from src.settings import Settings


class Container(containers.DeclarativeContainer):
    # Settings
    settings = providers.Singleton(Settings)
    endpoints = providers.Singleton(Endpoints, host=settings.provided.HOST)
    # DB Connection
    engine = providers.Singleton(create_async_engine, settings.provided.database_url, future=True, echo=True)
    sessionmaker = providers.Singleton(async_sessionmaker, engine, expire_on_commit=False)
    # Repository
    admin_repository = providers.Factory(AdminRepository, sessionmaker=sessionmaker)
    user_repository = providers.Factory(UserRepository, sessionmaker=sessionmaker)
    match_repository = providers.Factory(UsersMatchRepository, sessionmaker=sessionmaker)
    match_review_repository = providers.Factory(MatchReviewRepository, sessionmaker=sessionmaker)
    # Messages
    ask_for_random_coffee_message = providers.Factory(
        MessageForUsers,
        message_text="Хочешь ли принять участие в random coffee на следующей неделе?",
        endpoint_yes=endpoints.provided.add_to_meeting,
        endpoint_no=endpoints.provided.not_meeting,
    )
    ask_how_meeting_go_message = providers.Factory(
        MessageForUsers,
        message_text="Удалось ли вам встретиться?",
        endpoint_yes=endpoints.provided.match_review_is_complete,
        endpoint_no=endpoints.provided.match_review_is_not_complete,
    )
    # Services
    admin_service = providers.Factory(
        AdminService, admin_repository=admin_repository, admin_username=settings.provided.ADMIN_USERNAME
    )
    registration_service = providers.Factory(RegistrationService, user_repository=user_repository)
    matching_service = providers.Factory(
        MatchingService, user_repository=user_repository, match_repository=match_repository
    )
    week_routine_service = providers.Factory(
        NotifyService,
        user_repository=user_repository,
        match_repository=match_repository,
        match_review_repository=match_review_repository,
        endpoints=endpoints,
        direct_friday_message=ask_for_random_coffee_message,
        direct_wednesday_message=ask_how_meeting_go_message,
    )
    # Scheduler
    scheduler: AsyncIOScheduler = providers.Singleton(AsyncIOScheduler)
