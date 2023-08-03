from dependency_injector.wiring import Provide
from mmpy_bot import Bot, Settings
from plugins import MyPlugin

from depends import Container


def init_bot(settings=Provide[Container.Settings]):
    bot = Bot(
        settings=Settings(
            MATTERMOST_URL=settings.MATTERMOST_URL,
            MATTERMOST_PORT=settings.MATTERMOST_PORT,
            MATTERMOST_API_PATH=settings.MATTERMOST_API_PATH,
            BOT_TOKEN=settings.BOT_TOKEN,
            BOT_TEAM=settings.BOT_TEAM,
            SSL_VERIFY=settings.SSL_VERIFY,
        ),
        plugins=[MyPlugin()],
    )
    return bot


def start_bot():
    bot = init_bot()
    bot.run()
    return bot


start_bot()
