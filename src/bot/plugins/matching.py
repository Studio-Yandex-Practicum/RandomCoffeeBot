import re

from dependency_injector.wiring import Provide, inject
from mmpy_bot import Message, Plugin, listen_to

from src.bot.services.matching import MatchingService
from src.depends import Container


class Matching(Plugin):
    @listen_to("match", re.IGNORECASE)
    @inject
    async def test(self, message: Message, usermatch: MatchingService = Provide[Container.matching_service]) -> None:
        try:
            await usermatch.run_matching()
            self.driver.reply_to(message, "Создание пар завершено")
        except Exception as error:
            self.driver.reply_to(message, str(error))
