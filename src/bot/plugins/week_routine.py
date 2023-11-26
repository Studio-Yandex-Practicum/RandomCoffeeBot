import re

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dependency_injector.wiring import Provide, inject
from mmpy_bot import ActionEvent, Plugin, listen_to, listen_webhook

from src.bot.schemas import Actions, Attachment, Context, Integration
from src.bot.services.matching import MatchingService
from src.bot.services.notify_service import NotifyService
from src.core.db.models import MatchReviewAnswerEnum
from src.depends import Container
from src.endpoints import Endpoints

MONDAY_TIME_SENDING_MESSAGE = 10
DAY_OF_WEEK_MONDAY = "mon"
FRIDAY_TIME_SENDING_MESSAGE = 11
DAY_OF_WEEK_FRIDAY = "fri"
SUNDAY_TIME_SENDING_MESSAGE = 11
DAY_OF_WEEK_SUNDAY = "sun"
WEDNESDAY_TIME_SENDING_MESSAGE = 11
DAY_OF_WEEK_WEDNESDAY = "wed"


class WeekRoutine(Plugin):
    @inject
    def direct_friday_message(self, endpoints: Endpoints = Provide[Container.endpoints]):
        action_yes = Actions(
            id="yes",
            name="Да",
            type="button",
            integration=Integration(url=endpoints.add_to_meeting, context=Context(action="yes")),
        )

        action_no = Actions(
            id="No",
            name="Нет",
            type="button",
            integration=Integration(url=endpoints.not_meeting, context=Context(action="no")),
        )

        every_friday_message = Attachment(
            text="Хочешь ли принять участие в random coffee на следующей неделе?", actions=[action_yes, action_no]
        )
        return every_friday_message

    @listen_to("/notify_all_users", re.IGNORECASE)
    @inject
    async def test_notify_all_users(
        self, message, notify_service: NotifyService = Provide[Container.week_routine_service,]
    ):
        attachments = self.direct_friday_message()
        await notify_service.notify_all_users(
            plugin=self, attachments=attachments, title="Еженедельный пятничный опрос"
        )

    @listen_to("/monday_message", re.IGNORECASE)
    @inject
    async def test_monday_message(
        self, message, notify_service: NotifyService = Provide[Container.week_routine_service,]
    ):
        await notify_service.meeting_notifications(plugin=self)

    @inject
    def on_start(
        self,
        notify_service: NotifyService = Provide[Container.week_routine_service,],
        matching_service: MatchingService = Provide[Container.matching_service],
        scheduler: AsyncIOScheduler = Provide[Container.scheduler],
    ):
        attachments = self.direct_friday_message()

        scheduler.add_job(
            notify_service.notify_all_users,
            "cron",
            day_of_week=DAY_OF_WEEK_FRIDAY,
            hour=FRIDAY_TIME_SENDING_MESSAGE,
            kwargs=dict(plugin=self, attachments=attachments, title="Еженедельный пятничный опрос"),
        )
        scheduler.add_job(
            matching_service.run_matching,
            "cron",
            day_of_week=DAY_OF_WEEK_SUNDAY,
            hour=SUNDAY_TIME_SENDING_MESSAGE,
        )
        scheduler.add_job(
            notify_service.meeting_notifications,
            "cron",
            day_of_week=DAY_OF_WEEK_MONDAY,
            hour=MONDAY_TIME_SENDING_MESSAGE,
            kwargs=dict(plugin=self),
        )
        scheduler.start()

    @listen_to("/stop_jobs", re.IGNORECASE)
    @inject
    def cancel_jobs(self, message, scheduler=Provide[Container.scheduler,]):
        scheduler.shutdown()
        self.driver.reply_to(message, "All jobs cancelled.")

    @inject
    async def _change_user_status(
        self, user_id: str, notify_service: NotifyService = Provide[Container.week_routine_service,]
    ):
        await notify_service.set_waiting_meeting_status(user_id)

    @listen_webhook("set_waiting_meeting_status")
    async def add_to_meeting(
        self,
        event: ActionEvent,
    ):
        await self._change_user_status(event.user_id)
        self.driver.respond_to_web(
            event,
            {
                "update": {"message": "До встречи!", "props": {}},
            },
        )

    @listen_webhook("not_meeting")
    async def no(self, event: ActionEvent):
        self.driver.respond_to_web(
            event,
            {
                "update": {"message": "На следующей неделе отправлю новое предложение.", "props": {}},
            },
        )

    @inject
    def direct_wednesday_message(self, endpoints: Endpoints = Provide[Container.endpoints]):
        action_yes = Actions(
            id="yes",
            name="Да",
            type="button",
            integration=Integration(url=endpoints.answer_yes, context=Context(action="yes")),
        )

        action_no = Actions(
            id="No",
            name="Нет",
            type="button",
            integration=Integration(url=endpoints.answer_no, context=Context(action="no")),
        )

        every_wednesday_message = Attachment(text="Удалось ли вам встретиться?", actions=[action_yes, action_no])
        return every_wednesday_message

    @listen_webhook("match_review_answer_yes")
    async def answer_yes(
        self,
        event: ActionEvent,
    ):
        await self._save_user_answer(event.user_id, MatchReviewAnswerEnum.YES)
        self.driver.respond_to_web(
            event,
            {
                "update": {
                    "message": "Поделитесь итогами вашей встречи в канале "
                    '"Coffe на этой неделе", отправьте фото и '
                    "краткие эмоции, чтобы мотивировать других "
                    "поучаствовать в Random Coffee!",
                    "props": {},
                },
            },
        )

    @listen_webhook("match_review_answer_no")
    async def answer_no(
        self,
        event: ActionEvent,
    ):
        await self._save_user_answer(event.user_id, MatchReviewAnswerEnum.NO)
        user_nickname = await self._get_pair_nickname(event.user_id)
        self.driver.respond_to_web(
            event,
            {
                "update": {
                    "message": f"Неделя скоро закончится, не забудь "
                    f"познакомиться с новым человеком и провести "
                    f"время за классным разговором, напиши "
                    f"{user_nickname} точно ждёт вашей встречи",
                    "props": {},
                },
            },
        )

    @inject
    async def _save_user_answer(
        self, user_id: str, answer: str, notify_service: NotifyService = Provide[Container.week_routine_service,]
    ):
        await notify_service.set_match_review_answer(user_id, answer)

    @inject
    async def _get_pair_nickname(
        self, user_id: str, matching_service: MatchingService = Provide[Container.week_routine_service,]
    ) -> str:
        return await matching_service.get_match_pair_nickname(user_id)

    @listen_to("/wednesday_message", re.IGNORECASE)
    @inject
    async def test_wednesday_message(
        self, message: str, notify_service: NotifyService = Provide[Container.week_routine_service,]
    ):
        attachments = self.direct_wednesday_message()
        await notify_service.match_review_notifications(plugin=self, attachments=attachments)
