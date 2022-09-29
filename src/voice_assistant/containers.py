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

    movie_session = providers.Factory(
        movies.AsyncMoviesSession,
        base_url=config.NETFLIX_MOVIES_BASE_URL,
    )

    movie_client = providers.Singleton(
        movies.AsyncMovieClient,
        session=movie_session,
    )

    movie_repository = providers.Singleton(
        movies.MovieRepository,
        movie_client=movie_client,
    )

    # Domain -> Assistant

    intent_dispatcher = providers.Singleton(
        assistant.IntentDispatcher,
        movie_repository=movie_repository,
    )

    alice_service = providers.Factory(
        alice.AliceService,
        intent_dispatcher=intent_dispatcher,
    )

    assistant_dispatcher = providers.Singleton(
        assistant.AssistantProviderDispatcher,
        assistant_service_factory=providers.FactoryAggregate(
            provider_dict={
                assistant.AssistantProviderSlug.YANDEX_ALICE: alice_service,
            },
        ),
    )


def override_providers(container: Container) -> Container:
    """Перезаписывание провайдеров с помощью стабов."""
    if not container.config.USE_STUBS():
        return container
    container.movie_client.override(providers.Singleton(MovieClientStub))
    return container
