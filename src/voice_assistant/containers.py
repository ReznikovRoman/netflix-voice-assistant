from dependency_injector import containers, providers

from voice_assistant.config.logging import configure_logger
from voice_assistant.domain import assistant
from voice_assistant.domain.assistant import alice
from voice_assistant.integrations import movies
from voice_assistant.integrations.movies.stubs import MovieClientStub


class Container(containers.DeclarativeContainer):
    """Контейнер с зависимостями."""

    wiring_config = containers.WiringConfiguration()

    config = providers.Configuration()

    logging = providers.Resource(configure_logger)

    # Integrations

    movie_client = providers.Singleton(movies.MovieClient)

    movie_repository = providers.Singleton(
        movies.MovieRepository,
        movie_client=movie_client,
    )

    # Infrastructure

    # Domain -> Assistant

    alice_service = providers.Factory(alice.AliceService)

    assistant_dispatcher = providers.Singleton(
        assistant.AssistantProviderDispatcher,
        assistant_service_factory=providers.FactoryAggregate(
            provider_dict={
                assistant.AssistantProviderSlug.YANDEX_ALICE.value: alice_service,
            },
        ),
    )


def override_providers(container: Container) -> Container:
    """Перезаписывание провайдеров с помощью стабов."""
    if not container.config.USE_STUBS():
        return container
    container.movie_client.override(providers.Singleton(MovieClientStub))
    return container


async def dummy_resource() -> None:
    """Функция-ресурс для перезаписи в DI контейнере."""
