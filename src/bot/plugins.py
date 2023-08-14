import re

from dependency_injector.wiring import Container, Provide, inject
from mmpy_bot import Message, Plugin, listen_to
from src.bot.services.admin import AdminRegistration


class MyPlugin(Plugin):
    @listen_to("Привет")
    async def wake_up(self, message: Message):
        self.driver.reply_to(message, "Привет, я помогу организовать тебе random coffee")


@inject
class Admin(Plugin):
    @listen_to("Admin", re.IGNORECASE)
    async def admin(
            self, message: Message, admin_registration: AdminRegistration = Provide[Container.admin_registration]
    ):
        await admin_registration(
            username=message.sender_name,
            user_id=message.user_id
        )
