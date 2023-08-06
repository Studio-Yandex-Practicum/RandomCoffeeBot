import re

from dependency_injector.wiring import Container, Provide, inject
from mmpy_bot import Message, Plugin, listen_to

from src.bot.services.registration import RegistrationService


@inject
class Registration(Plugin):
    @listen_to("Register", re.IGNORECASE)
    async def Register(
        self, message: Message, registration: RegistrationService = Provide[Container.registration_service]
    ):
        self.driver.reply_to(message, "Please provide the following information: ...")
        registration.register("username", "first_name", "last_name")
