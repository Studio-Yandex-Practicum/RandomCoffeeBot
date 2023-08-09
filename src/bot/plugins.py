from mmpy_bot import Message, Plugin, listen_to


class MyPlugin(Plugin):  # type: ignore[misc]
    @listen_to("Привет")  # type: ignore[misc]
    async def wake_up(self, message: Message) -> Message:
        self.driver.reply_to(message, "Привет, я помогу организовать тебе random coffee")
