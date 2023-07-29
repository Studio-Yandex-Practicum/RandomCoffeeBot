from dependency_injector import containers, providers

from .settings import Settings


class Container(containers.DeclarativeContainer):
    settings = providers.Singleton(Settings)
