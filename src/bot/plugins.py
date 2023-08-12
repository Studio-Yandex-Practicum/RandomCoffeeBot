import re

from dependency_injector.wiring import Container, Provide, inject
from mmpy_bot import Message, Plugin, listen_to

from src.bot.services.registration import RegistrationService
from src.core.db.models import User


@inject
class Registration(Plugin):
    @listen_to("Register", re.IGNORECASE)
    async def Register(
        self, message: Message, registration: RegistrationService = Provide[Container.registration_service]
    ):
        user_instance = User(**self.driver.get_user_info(message.user_id))
        await registration.register(user_instance)
        self.driver.reply_to(message, "Регистрация завершена")
