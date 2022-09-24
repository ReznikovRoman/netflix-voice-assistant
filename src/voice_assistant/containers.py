from dependency_injector import containers, providers

from voice_assistant.config.logging import configure_logger
from voice_assistant.domain import assistant
from voice_assistant.domain.assistant import alice
from voice_assistant.integrations import movies
from voice_assistant.integrations.movies.stubs import MovieClientStub


async def dummy_resource() -> None:
    """Функция-ресурс для перезаписи в DI контейнере."""


class Container(containers.DeclarativeContainer):
    """Контейнер с зависимостями."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "voice_assistant.api.v1.handlers.assistant",
        ],
    )

    config = providers.Configuration()

    logging = providers.Resource(configure_logger)
    _delete_me = providers.Resource(dummy_resource)  # TODO: удалить после добавления асинхронного ресурса

    # Integrations

    movie_client = providers.Singleton(movies.MovieClient)

    movie_repository = providers.Singleton(
        movies.MovieRepository,
        movie_client=movie_client,
    )

    # Infrastructure

    # Domain -> Assistant
    intent_dispatcher_service = providers.Singleton(
        assistant.IntentDispatcher,
        movie_repository=movie_repository,
    )

    alice_service = providers.Factory(
        alice.AliceService,
        intent_dispatcher=intent_dispatcher_service,
    )

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
