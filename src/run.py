from dependency_injector.wiring import Provide
from mmpy_bot import Bot, Settings

from bot.plugins import MyPlugin
from depends import Container
from settings import Settings


def init_bot(config: Settings):
    bot = Bot(
        settings=Settings(
            MATTERMOST_URL=config.MATTERMOST_URL,
            MATTERMOST_PORT=config.MATTERMOST_PORT,
            MATTERMOST_API_PATH=config.MATTERMOST_API_PATH,
            BOT_TOKEN=config.BOT_TOKEN,
            BOT_TEAM=config.BOT_TEAM,
            SSL_VERIFY=config.SSL_VERIFY,
        ),
        plugins=[MyPlugin()],
    )
    bot.run()


if __name__ == "__main__":
    container = Container()
    bot = init_bot(container.settings())
