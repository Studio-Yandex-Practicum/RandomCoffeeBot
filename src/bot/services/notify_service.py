import structlog
from mattermostautodriver.exceptions import NotEnoughPermissions
from mmpy_bot import Plugin

from src.bot.schemas import Attachment
from src.core.db.repository.user import UserRepository

logger = structlog.get_logger()


class NotifyService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    async def notify_all_users(
        self, plugin: Plugin, attachments: Attachment, title: str = "Еженедельный опрос"
    ) -> None:
        """Функция отправки еженедельного сообщения (создания поста)"""

        users_id = await self._user_repository.get_all_chat_id()
        if not users_id:
            logger.error("Пользователи отсутствуют.")
            return None
        for user_id in users_id:
            try:
                logger.info(f"Началась отправка сообщения {user_id}")
                plugin.driver.create_post(
                    channel_id=user_id, message=title, props={"attachments": [attachments.model_dump()]}
                )
                logger.info("Сообщение отправлено.")
            except NotEnoughPermissions:
                logger.error(f"Пользователя с таким user_id {user_id} нет в matter_most")

    async def set_waiting_meeting_status(self, user_id: str) -> None:
        await self._user_repository.set_waiting_meeting_status(user_id)
