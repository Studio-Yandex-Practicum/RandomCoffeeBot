import re

import schedule
from dependency_injector.wiring import inject
from mmpy_bot import Message, Plugin, listen_to

from src.bot.constants.const_message import every_week_message, friday_time_sending_message
from src.settings import Settings


class WeekRoutine(Plugin):
    @inject
    def send_message(self, users_id=None, title: str = "Еженедельный опрос") -> None:
        """Функция отправки еженедельного сообщения (создания поста)"""
        if users_id is None:
            users_id = [Settings().CHANNEL_ID]
        for user_id in users_id:
            self.driver.create_post(channel_id=user_id, message=title, props={"attachments": [every_week_message]})

    @listen_to("send_asking_message", re.IGNORECASE)
    @inject
    def send_asking_message(self, message: Message):
        """Отправка сообщения по команде в канал"""
        self.send_message(title="Тестовая отправка")

    @listen_to("start_week_routines")
    @inject
    def week_routine(self, message):
        """Функция запуска еженедельных рутин"""

        users_id = [
            "iqgg313ew3fppydtet45myk5qa",  # получить список id пользователей.
        ]
        schedule.every().friday.at(friday_time_sending_message).do(self.send_message, users_id).tag("friday")

    @listen_to("stop jobs", re.IGNORECASE)
    def cancel_jobs(self, message):
        schedule.clear()
        self.driver.reply_to(message, "All jobs cancelled.")
