from random import choice

from dependency_injector.providers import Factory

from ...integrations.movies import MovieRepository
from .enums import AssistantProviderSlug, Message
from .exceptions import UnknownAssistantProvider
from .schemas import AssistantRequest, AssistantResponse, IntentChoice
from .services import AssistantService, get_assistant_service


class AssistantProviderDispatcher:
    """Диспатчер провайдеров голосового помощника."""

    def __init__(self, assistant_service_factory: Factory[AssistantService]) -> None:
        self._assistant_service_factory = assistant_service_factory

    async def dispatch_provider(self, provider: AssistantProviderSlug, /, *, data: dict) -> AssistantResponse:
        """Выбор корректного сервиса для данного провайдера голосового ассистента."""
        assistant_service = get_assistant_service(self._assistant_service_factory, provider=provider.value)
        provider_request = assistant_service.build_request_from_provider_data(data)
        match provider:
            case AssistantProviderSlug.YANDEX_ALICE:
                response = assistant_service.process_request(provider_request)
            case _:
                raise UnknownAssistantProvider()
        return response


class IntentDispatcher:
    """Диспатчер интентов."""

    def __init__(self, movie_repository: MovieRepository) -> None:
        self.movie_repository = movie_repository

    async def dispatcher_intent(self, assistant_request: AssistantRequest) -> AssistantResponse:
        """Выбор нужного обработчика по интенту."""

        async def get_film_description(search_value: str):
            film_id = await self.movie_repository.find_movie_by_name(search_value)
            film = await self.movie_repository.find_movie_by_id(film_id)
            return AssistantResponse(
                text=choice(Message.FILM_DESCRIPTION_MESSAGE_LIST.value).format(search_value, film),
            )

        async def get_actors_in_film(search_value: str):
            film_id = await self.movie_repository.find_movie_by_name(search_value)
            film = await self.movie_repository.find_movie_by_id(film_id)
            return AssistantResponse(
                text=choice(Message.ACTORS_IN_FILM_MESSAGE_LIST.value).format(search_value, film),
            )

        async def film_director(search_value: str):
            film_id = await self.movie_repository.find_movie_by_name(search_value)
            film = await self.movie_repository.find_movie_by_id(film_id)
            return AssistantResponse(
                text=choice(Message.FILM_DIRECTOR_MESSAGE_LIST.value).format(search_value, film.directors),
            )

        async def get_film_rating(search_value: str):
            film_by_name = await self.movie_repository.find_movie_by_name(search_value)
            film = await self.movie_repository.find_movie_by_id(film_by_name.film_id)
            return AssistantResponse(
                text=choice(Message.FILM_RATING_MESSAGE_LIST.value).format(search_value, film.imdb_rating),
            )

        async def search_by_director(search_value: str):
            film_id = await self.movie_repository.find_movie_by_name(search_value)
            film = await self.movie_repository.find_movie_by_id(film_id)
            return AssistantResponse(
                text=choice(Message.FIND_BY_DIRECTOR_MESSAGE_LIST.value).format(search_value, film),
            )

        async def not_recognized():
            # TODO доделать ответы
            response = "не понял"
            return response

        match assistant_request.intent:
            case IntentChoice.FILM_ACTORS:
                response = await get_actors_in_film(assistant_request.search_value)

            case IntentChoice.FILM_DESCRIPTION:
                response = await get_film_description(assistant_request.search_value)

            case IntentChoice.FILM_DIRECTORS:
                response = await film_director(assistant_request.search_value)

            case IntentChoice.SEARCH_BY_DIRECTOR:
                response = await search_by_director(assistant_request.search_value)

            case IntentChoice.FILM_RATING:
                response = await get_film_rating(assistant_request.search_value)

            case _:
                response = await not_recognized()

        return response
