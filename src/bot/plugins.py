import re

from dependency_injector.wiring import Container, Provide, inject
from mmpy_bot import Message, Plugin, listen_to

from src.bot.services.admin import AdminRegistration


class MyPlugin(Plugin):
    @listen_to("Привет")
    async def wake_up(self, message: Message):
        self.driver.reply_to(message, "Привет, я помогу организовать тебе random coffee")
