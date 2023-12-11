import re
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dependency_injector.wiring import Provide, inject
from mmpy_bot import ActionEvent, Plugin, listen_to, listen_webhook
from mmpy_bot.wrappers import Message

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
    def direct_friday_message(self, endpoints: Endpoints = Provide[Container.endpoints]) -> Attachment:
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
        self, message: Message, notify_service: NotifyService = Provide[Container.week_routine_service,]
    ) -> None:
        attachments = self.direct_friday_message()
        await notify_service.notify_all_users(
            plugin=self, attachments=attachments, title="Еженедельный пятничный опрос"
        )

    @listen_to("/monday_message", re.IGNORECASE)
    @inject
    async def test_monday_message(
        self, message: Message, notify_service: NotifyService = Provide[Container.week_routine_service,]
    ) -> None:
        await notify_service.meeting_notifications(plugin=self)

    @inject
    def on_start(
        self,
        notify_service: NotifyService = Provide[Container.week_routine_service,],
        matching_service: MatchingService = Provide[Container.matching_service],
        scheduler: AsyncIOScheduler = Provide[Container.scheduler],
    ) -> None:
        friday_attachments = self.direct_friday_message()

        scheduler.add_job(
            notify_service.notify_all_users,
            "cron",
            day_of_week=DAY_OF_WEEK_FRIDAY,
            hour=FRIDAY_TIME_SENDING_MESSAGE,
            kwargs=dict(plugin=self, attachments=friday_attachments, title="Еженедельный пятничный опрос"),
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
        scheduler.add_job(
            self.wednesday_notification_and_closing_meetings,
            "cron",
            day_of_week=DAY_OF_WEEK_WEDNESDAY,
            hour=WEDNESDAY_TIME_SENDING_MESSAGE,
            kwargs=dict(notify_service=notify_service, matching_service=matching_service),
        )
        scheduler.start()

    @listen_to("/stop_jobs", re.IGNORECASE)
    @inject
    def cancel_jobs(self, message: Message, scheduler: AsyncIOScheduler = Provide[Container.scheduler,]) -> None:
        scheduler.shutdown()
        self.driver.reply_to(message, "All jobs cancelled.")

    @inject
    async def _change_user_status(
        self, user_id: str, notify_service: NotifyService = Provide[Container.week_routine_service,]
    ) -> None:
        await notify_service.set_waiting_meeting_status(user_id)

    @listen_webhook("set_waiting_meeting_status")
    async def add_to_meeting(
        self,
        event: ActionEvent,
    ) -> None:
        await self._change_user_status(event.user_id)
        self.driver.respond_to_web(
            event,
            {
                "update": {"message": "До встречи!", "props": {}},
            },
        )

    @listen_webhook("not_meeting")
    async def no(self, event: ActionEvent) -> None:
        self.driver.respond_to_web(
            event,
            {
                "update": {"message": "На следующей неделе отправлю новое предложение.", "props": {}},
            },
        )

    @inject
    def direct_wednesday_message(self, endpoints: Endpoints = Provide[Container.endpoints]) -> Attachment:
        action_yes = Actions(
            id="yes",
            name="Да",
            type="button",
            integration=Integration(url=endpoints.match_review_is_complete, context=Context(action="yes")),
        )

        action_no = Actions(
            id="No",
            name="Нет",
            type="button",
            integration=Integration(url=endpoints.match_review_is_not_complete, context=Context(action="no")),
        )

        every_wednesday_message = Attachment(text="Удалось ли вам встретиться?", actions=[action_yes, action_no])
        return every_wednesday_message

    @listen_webhook("match_review_is_complete")
    async def answer_yes(
        self,
        event: ActionEvent,
    ) -> None:
        await self._save_user_answer(event.user_id, MatchReviewAnswerEnum.IS_COMPLETE)
        self.driver.respond_to_web(
            event,
            {
                "update": {
                    "message": "Поделитесь итогами вашей встречи в канале "
                    '"Coffee на этой неделе", отправьте фото и '
                    "краткие эмоции, чтобы мотивировать других "
                    "поучаствовать в Random Coffee!",
                    "props": {},
                },
            },
        )

    @listen_webhook("match_review_is_not_complete")
    async def answer_no(
        self,
        event: ActionEvent,
    ) -> None:
        await self._save_user_answer(event.user_id, MatchReviewAnswerEnum.IS_NOT_COMPLETE)
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
    ) -> None:
        await notify_service.set_match_review_answer(user_id, answer)

    @inject
    async def _get_pair_nickname(
        self, user_id: str, matching_service: MatchingService = Provide[Container.matching_service,]
    ) -> Any:
        return await matching_service.get_match_pair_nickname(user_id)

    @listen_to("/wednesday_message", re.IGNORECASE)
    @inject
    async def test_wednesday_message(
        self, message: str, notify_service: NotifyService = Provide[Container.week_routine_service,]
    ) -> None:
        attachments = self.direct_wednesday_message()
        await notify_service.match_review_notifications(plugin=self, attachments=attachments)

    async def wednesday_notification_and_closing_meetings(
        self,
        notify_service: NotifyService,
        matching_service: MatchingService,
    ) -> None:
        attachments = self.direct_wednesday_message()
        await notify_service.match_review_notifications(plugin=self, attachments=attachments)
        await matching_service.run_closing_meetings()
