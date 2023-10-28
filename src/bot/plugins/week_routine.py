import re

import structlog
from dependency_injector.wiring import Provide, inject
from mmpy_bot import ActionEvent, Plugin, WebHookEvent, listen_to, listen_webhook

from src.bot.schemas import Actions, Attachment, Context, Integration
from src.bot.services.notify_service import NotifyService
from src.depends import Container
from src.endpoints import Endpoints

FRIDAY_TIME_SENDING_MESSAGE = 11
DAY_OF_WEEK_FRI = "fri"
LOGGER = structlog.get_logger()


class WeekRoutine(Plugin):
    @inject
    def create_message(self, endpoints: Endpoints = Provide[Container.endpoints]):
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

    @inject
    def on_start(
        self,
        notify_service: NotifyService = Provide[Container.week_routine_service,],
        scheduler=Provide[Container.scheduler,],
    ):
        attachments = self.create_message()
        scheduler.add_job(
            notify_service.notify_all_users,
            "interval",
            seconds=20,
            kwargs=dict(plugin=self, attachments=attachments, title="Еженедельный пятничный опрос"),
        )
        # scheduler.add_job(
        #     notify_service.notify_all_users,
        #     "cron",
        #     day_of_week=DAY_OF_WEEK_FRI,
        #     hour=FRIDAY_TIME_SENDING_MESSAGE,
        #     kwargs=dict(plugin=self, attachments=attachments, title="Еженедельный пятничный опрос"),
        # )

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
        await notify_service.change_user_status(user_id)

    @listen_webhook("yes")
    async def add_to_meeting(
        self,
        event: WebHookEvent,
    ):
        if isinstance(event, ActionEvent):
            await self._change_user_status(event.channel_id)
            self.driver.respond_to_web(
                event,
                {
                    "update": {"message": "До встречи!", "props": {}},
                },
            )
        else:
            self.driver.create_post(event.body["channel_id"], f"Webhook '{event.webhook_id}' triggered!")

    @listen_webhook("no")
    async def no(self, event: WebHookEvent):
        if isinstance(event, ActionEvent):
            self.driver.respond_to_web(
                event,
                {
                    "update": {"message": "На следующей неделе отправлю новое предложение.", "props": {}},
                },
            )
        else:
            self.driver.create_post(event.body["channel_id"], f"Webhook '{event.webhook_id}' triggered!")
