from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dependency_injector.wiring import Provide, inject
from mmpy_bot import ActionEvent, Plugin, listen_webhook

from src.bot.services.matching import MatchingService
from src.bot.services.notify_service import NotifyService
from src.core.db.models import MatchReviewAnswerEnum
from src.depends import Container

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
    def on_start(
        self,
        notify_service: NotifyService = Provide[Container.week_routine_service,],
        matching_service: MatchingService = Provide[Container.matching_service],
        scheduler: AsyncIOScheduler = Provide[Container.scheduler],
    ) -> None:
        scheduler.add_job(
            notify_service.notify_all_users,
            "cron",
            day_of_week=DAY_OF_WEEK_FRIDAY,
            hour=FRIDAY_TIME_SENDING_MESSAGE,
            kwargs=dict(plugin=self, title="Еженедельный пятничный опрос"),
        )
        scheduler.add_job(
            self.run_matching_and_no_pair_messages,
            "cron",
            day_of_week=DAY_OF_WEEK_SUNDAY,
            hour=SUNDAY_TIME_SENDING_MESSAGE,
            kwargs=dict(notify_service=notify_service, matching_service=matching_service),
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

    async def wednesday_notification_and_closing_meetings(
        self,
        notify_service: NotifyService,
        matching_service: MatchingService,
    ) -> None:
        await notify_service.match_review_notifications(plugin=self)
        await matching_service.run_closing_meetings()

    async def run_matching_and_no_pair_messages(
        self,
        notify_service: NotifyService,
        matching_service: MatchingService,
    ) -> None:
        await matching_service.run_matching()
        await notify_service.send_no_pair_messages(plugin=self)
