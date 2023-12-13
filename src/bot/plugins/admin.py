import re
from functools import wraps
from typing import Any, Awaitable, Callable, TypeVar

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dependency_injector.wiring import Provide, inject
from mmpy_bot import Message, Plugin, listen_to

from src.bot.services.admin import AdminService
from src.bot.services.matching import MatchingService
from src.bot.services.notify_service import NotifyService
from src.core.db.models import Admin
from src.depends import Container

ReturningT = TypeVar("ReturningT", covariant=True)
Handler = Callable[..., Awaitable[ReturningT]]


def is_admin(fn: Handler[ReturningT]) -> Handler[ReturningT | None]:
    @wraps(fn)
    @inject
    async def wrapper(
        self: Plugin,
        message: Message,
        *args: Any,
        admin_service: AdminService = Provide[Container.admin_service],
    ) -> ReturningT | None:
        admin_instance = Admin(username=message.sender_name, user_id=message.user_id)
        if await admin_service.check_if_admin(message.user_id, admin_instance):
            return await fn(self, message, *args)
        else:
            self.driver.reply_to(message, "Недостаточно прав!")
        return None

    return wrapper


class BotAdmin(Plugin):
    @listen_to("notify_all_users", re.IGNORECASE)
    @is_admin
    @inject
    async def test_notify_all_users(
        self, message: Message, notify_service: NotifyService = Provide[Container.week_routine_service,]
    ) -> None:
        """Тестирование опроса по пятницам"""
        await notify_service.notify_all_users(plugin=self)

    @listen_to("monday_message", re.IGNORECASE)
    @is_admin
    @inject
    async def test_monday_message(
        self, message: Message, notify_service: NotifyService = Provide[Container.week_routine_service,]
    ) -> None:
        """Тестирование напоминания о встречах"""
        await notify_service.meeting_notifications(plugin=self)

    @listen_to("wednesday_message", re.IGNORECASE)
    @is_admin
    @inject
    async def test_wednesday_message(
        self, message: Message, notify_service: NotifyService = Provide[Container.week_routine_service,]
    ) -> None:
        """Тестирование опроса по средам"""
        await notify_service.match_review_notifications(plugin=self)

    @listen_to("match", re.IGNORECASE)
    @is_admin
    @inject
    async def test(
        self, message: Message, matching_service: MatchingService = Provide[Container.matching_service]
    ) -> None:
        """Тестирование создания пар"""
        try:
            reply_text = await matching_service.run_matching()
            self.driver.reply_to(message, reply_text)
        except Exception as error:
            self.driver.reply_to(message, str(error))

    @listen_to("close", re.IGNORECASE)
    @is_admin
    @inject
    async def test_closing_meetings(
        self, message: Message, matching_service: MatchingService = Provide[Container.matching_service]
    ) -> None:
        """Тестирование закрытия встреч"""
        try:
            await matching_service.run_closing_meetings()
            self.driver.reply_to(message, "Встречи закрыты")
        except Exception as error:
            self.driver.reply_to(message, str(error))

    @listen_to("stop_jobs", re.IGNORECASE)
    @is_admin
    @inject
    async def cancel_jobs(self, message: Message, scheduler: AsyncIOScheduler = Provide[Container.scheduler,]) -> None:
        """Остановка всех jobs"""
        scheduler.shutdown()
        self.driver.reply_to(message, "All jobs cancelled.")
