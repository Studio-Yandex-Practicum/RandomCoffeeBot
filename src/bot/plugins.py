from mmpy_bot import Message, Plugin, listen_to


class MyPlugin(Plugin):
    @listen_to("Привет")
    async def wake_up(self, message: Message):
        await self.driver.reply_to(message, "Привет, я помогу организовать тебе random coffee")