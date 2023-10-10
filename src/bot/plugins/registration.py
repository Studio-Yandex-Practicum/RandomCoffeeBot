import re

from dependency_injector.wiring import Provide, inject
from mmpy_bot import Message, Plugin, listen_to

from src.bot.services.registration import RegistrationService
from src.core.db.models import User
from src.depends import Container


class Registration(Plugin):
    @listen_to("Register", re.IGNORECASE)
    @inject
    async def register(
        self, message: Message, registration: RegistrationService = Provide[Container.registration_service]
    ) -> None:
        user_data = self.driver.get_user_info(message.user_id)
        user_instance = User(
            username=user_data["username"], first_name=user_data["first_name"], last_name=user_data["last_name"]
        )
        await registration.register(user_instance)
        self.driver.reply_to(message, "Регистрация завершена")
