from dependency_injector.wiring import Provide, inject
from mmpy_bot import Plugin

from src.depends import Container


class CommandRegistration(Plugin):
    @inject
    def on_start(
        self,
        settings=Provide(Container.settings),
    ) -> None:
        self.driver.commands.create_command(
            options={
                "team_id": settings.CHANNEL_ID,
                "method": "G",
                "trigger": "rand",
                "url": "https://www.random.org/integers/?num=1&min=1&max=100&col=1&base=10&format=plain&rnd=new&cl=w",
            }
        )
