from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    """Основа класса контейнера."""

    config = providers.Configuration()
    pass
