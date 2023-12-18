from typing import Any

from src.bot.schemas import Actions, Attachment, Context, Integration
from src.endpoints import Endpoints


class MessageForUsers:
    def __init__(self, message_text: str, endpoint_yes: str, endpoint_no: str) -> None:
        self.action_yes = Actions(
            id="yes",
            name="Да",
            type="button",
            integration=Integration(url=endpoint_yes, context=Context(action="yes")),
        )
        self.action_no = Actions(
            id="No",
            name="Нет",
            type="button",
            integration=Integration(url=endpoint_no, context=Context(action="no")),
        )
        self.message = Attachment(text=message_text, actions=[self.action_yes, self.action_no])

    def return_message(self) -> dict[str, Any]:
        return self.message.model_dump()


class FridayMessage(MessageForUsers):
    def __init__(self, endpoints: Endpoints):
        self._endpoints = endpoints
        super().__init__(
            message_text="Хочешь ли принять участие в random coffee на следующей неделе?",
            endpoint_yes=self._endpoints.add_to_meeting,
            endpoint_no=self._endpoints.not_meeting,
        )


class WednesdayMessage(MessageForUsers):
    def __init__(self, endpoints: Endpoints):
        self._endpoints = endpoints
        super().__init__(
            message_text="Удалось ли вам встретиться?",
            endpoint_yes=self._endpoints.match_review_is_complete,
            endpoint_no=self._endpoints.match_review_is_not_complete,
        )
