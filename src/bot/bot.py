from mmpy_bot import Bot, Settings

from bot.plugins import MyPlugin
from settings import Settings as Settings_bot


def init_bot(config: Settings_bot) -> Bot:
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
    return bot
