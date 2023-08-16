import structlog

from src.bot.bot import init_bot
from src.core.logging import init_logging

from .depends import Container

log = structlog.get_logger()


def main() -> None:
    container = Container()
    container.wire(packages=("src",))
    init_logging(container.settings())
    bot = init_bot(container.settings())
    log.info("Application started")
    bot.run()


if __name__ == "__main__":
    main()
