from mmpy_bot import Bot, Settings
from plugins import MyPlugin


def init_bot():
    bot = Bot(
        settings=Settings(
            MATTERMOST_URL="http://mattermost",
            MATTERMOST_PORT=8065,
            MATTERMOST_API_PATH="/api/v4",
            BOT_TOKEN="<your_bot_token>",
            BOT_TEAM="<team_name>",
            SSL_VERIFY=False,
        ),
        plugins=[MyPlugin()],
    )
    return bot


def start_bot():
    bot = init_bot()
    bot.run()
    return bot


start_bot()
