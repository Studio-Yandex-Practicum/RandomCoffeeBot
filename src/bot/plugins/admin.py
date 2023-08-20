import re

from dependency_injector.wiring import Provide, inject
from mmpy_bot import Message, Plugin, listen_to

from src.bot.services.admin import AdminService
from src.core.db.models import Admin
from src.depends import Container


class BotAdmin(Plugin):
    @listen_to("Admin", re.IGNORECASE)
    @inject
    async def admin(self, message: Message, admin_service: AdminService = Provide[Container.admin_service]):
        admin_instance = Admin(username=message.sender_name, user_id=message.user_id)
        if await admin_service.check_if_admin(message.sender_name, message.user_id, admin_instance):
            self.driver.reply_to(message, "Привет, админ!")
        else:
            self.driver.reply_to(message, "Недостаточно прав!")
