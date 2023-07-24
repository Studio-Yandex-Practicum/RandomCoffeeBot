from mmpy_bot import Bot, Settings

from plugins import MyPlugin


def init_bot():
    bot = Bot(
        settings=Settings(
            MATTERMOST_URL="mattermost",
            MATTERMOST_PORT=8065,
            MATTERMOST_API_PATH='/api/v4',
            BOT_TOKEN="8o38jyaqc784xf7jnes1r4jq5o",
            BOT_TEAM="Coffee",
            SSL_VERIFY=False,
        ),
        plugins=[MyPlugin()],
    )
    return bot


async def start_bot():
    bot = init_bot()
    await bot.run()
    return bot

