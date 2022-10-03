from dependency_injector import containers, providers
from netflix.movies import client as movie_client
from netflix.movies.client.stubs import MovieClientStub

from voice_assistant.config.logging import configure_logger
from voice_assistant.domain import assistant
from voice_assistant.domain.assistant import alice
from voice_assistant.integrations import movies


async def dummy_resource() -> None:
    """Dummy async resource for overriding providers in a DI container."""


class Container(containers.DeclarativeContainer):
    """DI container."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "voice_assistant.api.v1.handlers.assistant",
        ],
    )

    config = providers.Configuration()

    logging = providers.Resource(configure_logger)
    _delete_me = providers.Resource(dummy_resource)  # TODO: remove after adding an async resource

    # Integrations

    movie_session = providers.Factory(
        movie_client.AsyncMovieSession,
        base_url=config.NETFLIX_MOVIES_BASE_URL,
    )

    movie_client = providers.Singleton(
        movie_client.AsyncMovieClient,
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
    """Overriding providers with stubs."""
    if not container.config.USE_STUBS():
        return container
    container.movie_client.override(providers.Singleton(MovieClientStub))
    return container
