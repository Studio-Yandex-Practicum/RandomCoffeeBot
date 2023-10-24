import re

import structlog
from dependency_injector.wiring import Provide, inject
from mmpy_bot import ActionEvent, Plugin, WebHookEvent, listen_to, listen_webhook

from src.bot.schemas import Action, Actions, Attachment, Integration
from src.bot.services.notify_service import NotifyService
from src.depends import Container

FRIDAY_TIME_SENDING_MESSAGE = 11
DAY_OF_WEEK_FRI = "fri"
LOGGER = structlog.get_logger()


class WeekRoutine(Plugin):
    action_yes = Actions(
        id="Yes",
        name="Да",
        type="button",
        integration=Integration(
            url="http://127.0.0.1:8579/hooks/add_to_meeting", context=Action(action="add_to_meeting")
        ),
    )

    action_no = Actions(
        id="No", name="Нет", type="button", integration=Integration(url="", context=Action(action="no"))
    )

    every_friday_message = Attachment(
        text="Хочешь ли принять участие в random coffee на следующей неделе?", actions=[action_yes, action_no]
    )

    @inject
    def on_start(
        self,
        notify_service: NotifyService = Provide[Container.week_routine_service,],
        scheduler=Provide[Container.scheduler,],
    ):
        scheduler.add_job(
            notify_service.notify_all_users,
            "interval",
            seconds=20,
            kwargs=dict(plugin=self, attachments=self.every_friday_message, title="Еженедельный пятничный опрос"),
        )
        # scheduler.add_job(
        #     notify_service.notify_all_users,
        #     "cron",
        #     day_of_week=DAY_OF_WEEK_FRI,
        #     hour=FRIDAY_TIME_SENDING_MESSAGE,
        #     kwargs=dict(plugin=self, attachments=self.every_friday_message, title="Еженедельный пятничный опрос"),
        # )

        scheduler.start()

    @listen_to("/stop_jobs", re.IGNORECASE)
    @inject
    def cancel_jobs(self, message, scheduler=Provide[Container.scheduler,]):
        scheduler.shutdown()
        self.driver.reply_to(message, "All jobs cancelled.")

    @listen_webhook("add_to_meeting")
    async def add_to_meeting(self, event: WebHookEvent):
        if isinstance(event, ActionEvent):
            self.driver.respond_to_web(
                event,
                {
                    # You can add any kind of JSON-serializable data here
                    "message": "hello!",
                },
            )
        else:
            self.driver.create_post(event.body["channel_id"], f"Webhook {event.webhook_id} triggered!")
