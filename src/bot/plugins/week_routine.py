import re

import schedule
from dependency_injector.wiring import inject
from mmpy_bot import Message, Plugin, listen_to

from src.bot.constants.const_message import every_week_message
from src.settings import Settings


class WeekRoutine(Plugin):
    @inject
    def send_message(
        self,
        users_id=None,
    ) -> None:
        if users_id is None:
            users_id = list(Settings().CHANNEL_ID)
        for user_id in users_id:
            self.driver.create_post(
                channel_id=user_id, message="Еженедельный опрос", props={"attachments": [every_week_message]}
            )

    @listen_to("send_asking_message", re.IGNORECASE)
    @inject
    def send_asking_message(self, message: Message):
        self.send_message()

    @listen_to("start_week_routine")
    @inject
    def week_routine(self, message):
        users_id = [
            "iqgg313ew3fppydtet45myk5qa",
        ]
        schedule.every(20).seconds.do(self.send_message, users_id)

    @listen_to("stop jobs", re.IGNORECASE)
    def cancel_jobs(self, message):
        schedule.clear()
        self.driver.reply_to(message, "All jobs cancelled.")
