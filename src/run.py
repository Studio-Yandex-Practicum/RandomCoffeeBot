import structlog

from src.bot.bot import init_bot
from src.depends import Container

log = structlog.get_logger()


def main():
    container = Container()
    container.wire(packages=("src",))
    bot = init_bot(container.settings())
    log.info("Application started")
    bot.run()


if __name__ == "__main__":
    main()
