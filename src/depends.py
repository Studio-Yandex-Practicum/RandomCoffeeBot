from dependency_injector import containers, providers
from dependency_injector.wiring import Provide

from .settings import Settings


class Container(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)


settings = Provide[Container.settings]
