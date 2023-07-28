from mmpy_bot import Bot, Settings
from plugins import MyPlugin

from depends import settings


def init_bot():
    bot = Bot(
        settings=Settings(
            MATTERMOST_URL=settings.mattermost_url,
            MATTERMOST_PORT=settings.mattermost_port,
            MATTERMOST_API_PATH=settings.mattermost_api_path,
            BOT_TOKEN=settings.bot_token,
            BOT_TEAM=settings.bot_team,
            SSL_VERIFY=settings.ssl_verify,
        ),
        plugins=[MyPlugin()],
    )
    return bot


def start_bot():
    bot = init_bot()
    bot.run()
    return bot


start_bot()
