from bot.bot import init_bot
from depends import Container

if __name__ == "__main__":
    container = Container()
    bot = init_bot(container.settings())
