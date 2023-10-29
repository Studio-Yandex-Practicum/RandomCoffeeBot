import re

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dependency_injector.wiring import Provide, inject
from mmpy_bot import Plugin, listen_to

from src.bot.schemas import Action, Actions, Attachment, Integration
from src.bot.services.matching import MatchingService
from src.bot.services.notify_service import NotifyService
from src.depends import Container

MONDAY_TIME_SENDING_MESSAGE = 10
DAY_OF_WEEK_MON = "mon"
FRIDAY_TIME_SENDING_MESSAGE = 11
DAY_OF_WEEK_FRI = "fri"
SUNDAY_TIME_SENDING_MESSAGE = 11
DAY_OF_WEEK_SUN = "sun"


class WeekRoutine(Plugin):
    action_yes = Actions(
        id="Yes", name="Да", type="botton", integration=Integration(url="", context=Action(action="yes"))
    )

    action_no = Actions(
        id="No", name="Нет", type="botton", integration=Integration(url="", context=Action(action="no"))
    )

    every_friday_message = Attachment(
        text="Хочешь ли принять участие в random coffee на следующей неделе?", actions=[action_yes, action_no]
    )

    @inject
    def on_start(
        self,
        notify_service: NotifyService = Provide[Container.week_routine_service,],
        matching_service: MatchingService = Provide[Container.matching_service],
        scheduler: AsyncIOScheduler = Provide[Container.scheduler],
    ):
        scheduler.add_job(
            notify_service.notify_all_users,
            "cron",
            day_of_week=DAY_OF_WEEK_FRI,
            hour=FRIDAY_TIME_SENDING_MESSAGE,
            kwargs=dict(plugin=self, attachments=self.every_friday_message, title="Еженедельный пятничный опрос"),
        )
        scheduler.add_job(
            matching_service.run_matching,
            "cron",
            day_of_week=DAY_OF_WEEK_SUN,
            hour=SUNDAY_TIME_SENDING_MESSAGE,
        )
        scheduler.add_job(
            notify_service.meeting_notifications,
            "cron",
            day_of_week=DAY_OF_WEEK_MON,
            hour=MONDAY_TIME_SENDING_MESSAGE,
            kwargs=dict(plugin=self),
        )
        scheduler.start()

    @listen_to("/stop_jobs", re.IGNORECASE)
    def cancel_jobs(self, message, scheduler=Provide[Container.scheduler]):
        scheduler.shutdown()
        self.driver.reply_to(message, "All jobs cancelled.")
