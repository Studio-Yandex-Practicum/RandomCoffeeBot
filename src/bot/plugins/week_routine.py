import re

import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dependency_injector.wiring import Provide, inject
from mmpy_bot import Message, Plugin, listen_to

from src.bot.schemas import Action, Actions, Attachment, Integration
from src.bot.services.week_routine import WeekRoutineService
from src.depends import Container

FRIDAY_TIME_SENDING_MESSAGE = 11
DAY_OF_WEEK_FRI = "fri"
LOGGER = structlog.get_logger()
SCHEDULER = AsyncIOScheduler()


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

    @listen_to("send_asking_message", re.IGNORECASE)
    @inject
    async def send_asking_message(
        self, message: Message, routine: WeekRoutineService = Provide[Container.week_routine_service]
    ):
        """Отправка сообщения по команде в канал"""
        await routine.send_message(self, attachments=self.every_friday_message, title="Тестовая отправка")

    @inject
    async def start_routine(
        self,
        routine: WeekRoutineService = Provide[Container.week_routine_service],
        attachments: Attachment = every_friday_message,
        title: str = "Еженедельный опрос",
    ):
        """Функция запуска еженедельных рутин"""
        await routine.send_message(self, attachments=attachments, title=title)

    def on_start(self):
        SCHEDULER.add_job(
            self.start_routine,
            "cron",
            day_of_week=DAY_OF_WEEK_FRI,
            hour=FRIDAY_TIME_SENDING_MESSAGE,
            kwargs=dict(attachments=self.every_friday_message, title="Еженедельный пятничный опрос"),
        )
        # -----------------------------------для теста:
        # SCHEDULER.add_job(
        #     self.start_routine,
        #     'interval', seconds=20,
        #     kwargs=dict(
        #         attachments=self.every_friday_message,
        #         title="Еженедельный пятничный опрос"
        #     )
        # )
        # -----------------------------------

        SCHEDULER.start()

    @listen_to("stop jobs", re.IGNORECASE)
    def cancel_jobs(self, message):
        SCHEDULER.shutdown()
        self.driver.reply_to(message, "All jobs cancelled.")
