from mmpy_bot import Bot, Settings
from .bot import MyPlugin

bot = Bot(
    settings=Settings(
        MATTERMOST_URL = "http://127.0.0.1",
        MATTERMOST_PORT = 8065,
        BOT_TOKEN = "<your_bot_token>",
        BOT_TEAM = "<team_name>",
        SSL_VERIFY = False,
    ),  # Either specify your settings here or as environment variables.
    plugins=[MyPlugin()],  # Add your own plugins here.
)
bot.run()