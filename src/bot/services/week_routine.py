import structlog
from mattermostautodriver.exceptions import NotEnoughPermissions

from src.bot.schemas import Attachment
from src.core.db.repository.user import UserRepository

logger = structlog.get_logger()


class WeekRoutineService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    async def send_message(self, plugin, attachments: Attachment, users_id=None, title: str = "Еженедельный опрос"):
        """Функция отправки еженедельного сообщения (создания поста)"""

        if users_id is None:
            users_id = await self._user_repository.get_all_chat_id()
        for user_id in users_id:
            try:
                logger.info(f"Началась отправка сообщения {user_id}")
                plugin.driver.create_post(
                    channel_id=user_id, message=title, props={"attachments": [attachments.model_dump()]}
                )
                logger.info("Сообщение отправлено.")
            except NotEnoughPermissions:
                logger.error(f"Пользователя с таким user_id {user_id} нет в matter_most")
