import re
from dataclasses import dataclass, fields

from dependency_injector.wiring import Provide, inject
from mmpy_bot import Message, Plugin, listen_to

from ..core.db.models import User
from ..depends import Container
from .services.registration import RegistrationService


@dataclass
class MattermostUserRegistrationInfo:
    username: str
    first_name: str
    last_name: str

    @classmethod
    def from_dict(cls, user_data: dict[str, str]) -> MattermostUserRegistrationInfo:  # noqa: F821
        return cls(
            **{attr: value for attr, value in user_data.items() if attr in (field.name for field in fields(cls))}
        )


@inject
class Registration(Plugin):
    @listen_to("Register", re.IGNORECASE)
    async def Register(
        self, message: Message, registration: RegistrationService = Provide[Container.registration_service]
    ) -> None:
        user_info = MattermostUserRegistrationInfo.from_dict(**self.driver.get_user_info(message.user_id))
        user_instance = User(
            username=user_info.username, first_name=user_info.first_name, last_name=user_info.last_name
        )
        await registration.register(user_instance)
        self.driver.reply_to(message, "Регистрация завершена")
