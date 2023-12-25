from typing import Any

from src.bot.schemas import Actions, Attachment, Context, Integration


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
