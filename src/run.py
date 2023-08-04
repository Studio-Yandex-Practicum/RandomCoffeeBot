from dependency_injector.wiring import inject

from bot.bot import init_bot
from depends import Container


@inject
def main():
    container = Container()
    container.wire(packages=("src",))
    bot = init_bot(container.settings())
    bot.run()


if __name__ == "__main__":
    main()
