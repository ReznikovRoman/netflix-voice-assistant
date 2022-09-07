from dependency_injector import containers, providers

from voice_assistant.config.logging import configure_logger


class Container(containers.DeclarativeContainer):
    """Контейнер с зависимостями."""

    wiring_config = containers.WiringConfiguration()

    config = providers.Configuration()

    logging = providers.Resource(configure_logger)


def override_providers(container: Container) -> Container:
    """Перезаписывание провайдеров с помощью стабов."""
    if not container.config.USE_STUBS():
        return container
    return container


async def dummy_resource() -> None:
    """Функция-ресурс для перезаписи в DI контейнере."""
