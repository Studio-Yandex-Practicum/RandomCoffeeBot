import structlog
from mattermostautodriver.exceptions import InvalidOrMissingParameters
from mmpy_bot import Plugin

from src.bot.services.create_message_service import MessageForUsers
from src.core.db.models import MatchStatusEnum, User
from src.core.db.repository.match_review import MatchReviewRepository
from src.core.db.repository.user import UserRepository
from src.core.db.repository.usersmatch import UsersMatchRepository
from src.endpoints import Endpoints

logger = structlog.get_logger()


class NotifyService:
    def __init__(
        self,
        user_repository: UserRepository,
        match_repository: UsersMatchRepository,
        match_review_repository: MatchReviewRepository,
        endpoints: Endpoints,
        direct_friday_message: MessageForUsers,
        direct_wednesday_message: MessageForUsers,
    ) -> None:
        self._user_repository = user_repository
        self._match_repository = match_repository
        self._match_review_repository = match_review_repository
        self._endpoints = endpoints
        self._direct_friday_message = direct_friday_message
        self._direct_wednesday_message = direct_wednesday_message

    async def notify_all_users(self, plugin: Plugin, title: str = "Еженедельный опрос") -> None:
        """Функция отправки еженедельного сообщения (создания поста)"""

        friday_attachments = self._direct_friday_message.return_message()
        users_id = await self._user_repository.get_all_chat_id()
        if not users_id:
            logger.error("Пользователи отсутствуют.")
            return None
        for user_id in users_id:
            try:
                plugin.driver.direct_message(
                    receiver_id=user_id, message=title, props={"attachments": [friday_attachments]}
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
                        message=f"Твои встречи на неделю: {user_two.first_name} {user_two.last_name} @{user_two.username}",
                    )
                except InvalidOrMissingParameters as error:
                    logger.error(str(error))

    async def set_match_review_answer(self, user_id: str, answer: str) -> None:
        match = await self._match_repository.get_by_user_id(user_id)
        await self._match_review_repository.set_match_review_answer(match, user_id, answer)

    async def match_review_notifications(
        self,
        plugin: Plugin,
        title: str = "Опрос по результатам встречи",
    ) -> None:
        attachments = self._direct_wednesday_message.return_message()
        for match in await self._match_repository.get_by_status(status=MatchStatusEnum.ONGOING):
            pair: list[User] = [match.object_user_one, match.object_user_two]
            for user_one, user_two in zip(pair, pair[::-1]):
                try:
                    plugin.driver.direct_message(
                        receiver_id=user_one.user_id, message=title, props={"attachments": [attachments]}
                    )
                except InvalidOrMissingParameters as error:
                    logger.error(str(error))
