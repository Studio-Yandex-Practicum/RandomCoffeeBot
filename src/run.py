import structlog

from bot.bot import init_bot
from depends import Container
from src.core import init_logging


log = structlog.get_logger()


def main():
    container = Container()
    container.wire(packages=("src",))
    init_logging()
    bot = init_bot(container.settings())
    log.info("Application started")
    bot.run()


if __name__ == "__main__":
    main()
