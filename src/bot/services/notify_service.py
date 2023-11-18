import structlog
from mattermostautodriver.exceptions import NotEnoughPermissions, InvalidOrMissingParameters
from mmpy_bot import Plugin

from src.bot.schemas import Attachment
from src.core.db.models import MatchStatusEnum, User
from src.core.db.repository.user import UserRepository
from src.core.db.repository.usersmatch import UsersMatchRepository

logger = structlog.get_logger()


class NotifyService:
    def __init__(self, user_repository: UserRepository, match_repository: UsersMatchRepository) -> None:
        self._user_repository = user_repository
        self._match_repository = match_repository

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
                plugin.driver.direct_message(
                    receiver_id=user_id, message=title, props={"attachments": [attachments.model_dump()]}
                )
            except InvalidOrMissingParameters:
                logger.error(f"Пользователя с таким user_id {user_id} нет в matter_most")

    async def set_waiting_meeting_status(self, user_id: str) -> None:
        await self._user_repository.set_waiting_meeting_status(user_id)

    async def meeting_notifications(self, plugin: Plugin) -> None:
        """Уведомляет участников встреч о паре на этой неделе."""
        for match in await self._match_repository.get_by_status(status=MatchStatusEnum.ONGOING):
            pair: list[User] = [match.object_user_one, match.object_user_two]
            for user_one, user_two in zip(pair, pair[::-1]):
                try:
                    plugin.driver.direct_message(
                        receiver_id=user_one.user_id,
                        message=f"Твои встречи на неделю: {user_two.first_name} {user_two.last_name}",
                    )
                except InvalidOrMissingParameters as error:
                    logger.error(str(error))
