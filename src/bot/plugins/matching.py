import re

from dependency_injector.wiring import Provide, inject
from mmpy_bot import Message, Plugin, listen_to

from src.bot.services.matching import MatchingService
from src.depends import Container


class Matching(Plugin):
    @listen_to("/match", re.IGNORECASE)
    @inject
    async def test(
        self, message: Message, matching_service: MatchingService = Provide[Container.matching_service]
    ) -> None:
        try:
            await matching_service.run_matching()
            self.driver.reply_to(message, "Создание пар завершено")
        except Exception as error:
            self.driver.reply_to(message, str(error))

    @listen_to("/close", re.IGNORECASE)
    @inject
    async def test_closing_meetings(
        self, message: Message, matching_service: MatchingService = Provide[Container.matching_service]
    ) -> None:
        try:
            await matching_service.run_closing_meetings()
            self.driver.reply_to(message, "Встречи закрыты")
        except Exception as error:
            self.driver.reply_to(message, str(error))
