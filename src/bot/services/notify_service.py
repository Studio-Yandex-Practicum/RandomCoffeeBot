import structlog
from dependency_injector.wiring import inject
from mattermostautodriver.exceptions import InvalidOrMissingParameters
from mmpy_bot import Plugin

from src.bot.schemas import Actions, Attachment, Context, Integration
from src.core.db.models import MatchStatusEnum, StatusEnum, User
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
    ) -> None:
        self._user_repository = user_repository
        self._match_repository = match_repository
        self._match_review_repository = match_review_repository
        self._endpoints = endpoints

    @inject
    def direct_friday_message(self) -> Attachment:
        action_yes = Actions(
            id="yes",
            name="Да",
            type="button",
            integration=Integration(url=self._endpoints.add_to_meeting, context=Context(action="yes")),
        )

        action_no = Actions(
            id="No",
            name="Нет",
            type="button",
            integration=Integration(url=self._endpoints.not_meeting, context=Context(action="no")),
        )

        every_friday_message = Attachment(
            text="Хочешь ли принять участие в random coffee на следующей неделе?", actions=[action_yes, action_no]
        )
        return every_friday_message

    async def notify_all_users(self, plugin: Plugin, title: str = "Еженедельный опрос") -> None:
        """Функция отправки еженедельного сообщения (создания поста)"""

        friday_attachments = self.direct_friday_message()
        users_id = await self._user_repository.get_all_chat_id()
        if not users_id:
            logger.error("Пользователи отсутствуют.")
            return None
        for user_id in users_id:
            try:
                plugin.driver.direct_message(
                    receiver_id=user_id, message=title, props={"attachments": [friday_attachments.model_dump()]}
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

    @inject
    def direct_wednesday_message(self) -> Attachment:
        action_yes = Actions(
            id="yes",
            name="Да",
            type="button",
            integration=Integration(url=self._endpoints.match_review_is_complete, context=Context(action="yes")),
        )

        action_no = Actions(
            id="No",
            name="Нет",
            type="button",
            integration=Integration(url=self._endpoints.match_review_is_not_complete, context=Context(action="no")),
        )

        every_wednesday_message = Attachment(text="Удалось ли вам встретиться?", actions=[action_yes, action_no])
        return every_wednesday_message

    async def match_review_notifications(
        self,
        plugin: Plugin,
        title: str = "Опрос по результатам встречи",
    ) -> None:
        attachments = self.direct_wednesday_message()
        for match in await self._match_repository.get_by_status(status=MatchStatusEnum.ONGOING):
            pair: list[User] = [match.object_user_one, match.object_user_two]
            for user_one, user_two in zip(pair, pair[::-1]):
                try:
                    plugin.driver.direct_message(
                        receiver_id=user_one.user_id, message=title, props={"attachments": [attachments.model_dump()]}
                    )
                except InvalidOrMissingParameters as error:
                    logger.error(str(error))

    async def send_no_pair_messages(self, plugin: Plugin) -> None:
        for user in await self._user_repository.get_by_status(status=StatusEnum.WAITING_MEETING):
            await self._user_repository.set_not_involved_status(user_id=user.id)
            try:
                plugin.driver.direct_message(
                    receiver_id=user.user_id,
                    message="К сожалению на этой неделе тебе не нашлось пары,"
                    " но мы уверены, что тебе обязательно повезёт на "
                    "следующей неделе!",
                )
            except InvalidOrMissingParameters as error:
                logger.error(str(error))
