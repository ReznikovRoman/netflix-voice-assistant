from random import choice

from dependency_injector.providers import Factory

from src.voice_assistant.integrations.movies import MovieRepository

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
        provider_request = await assistant_service.build_request_from_provider_data(data)
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

    async def get_film_description(self, search_query: str):
        film_short_detail = await self.movie_repository.find_movie_by_name(search_query)
        film_detail = await self.movie_repository.find_movie_by_id(film_short_detail.film_id)
        return AssistantResponse(
            text=choice(Message.FILM_DESCRIPTION_MESSAGE_LIST.value).format(
                film=search_query,
                description=film_detail.description,
            ),
        )

    async def get_film_actors(self, search_query: str):
        film_short_detail = await self.movie_repository.find_movie_by_name(search_query)
        film_detail = await self.movie_repository.find_movie_by_id(film_short_detail.film_id)
        return AssistantResponse(
            text=choice(Message.ACTORS_IN_FILM_MESSAGE_LIST.value).format(
                film=search_query,
                actors=film_detail.actors,
            ),
        )

    async def get_film_directors(self, search_query: str):
        film_short_detail = await self.movie_repository.find_movie_by_name(search_query)
        film_detail = await self.movie_repository.find_movie_by_id(film_short_detail.film_id)
        return AssistantResponse(
            text=choice(Message.FILM_DIRECTOR_MESSAGE_LIST.value).format(
                film=search_query,
                director=film_detail.directors,
            ),
        )

    async def get_film_rating(self, search_query: str):
        film_short_detail = await self.movie_repository.find_movie_by_name(search_query)
        return AssistantResponse(
            text=choice(Message.FILM_RATING_MESSAGE_LIST.value).format(
                film=search_query,
                rating=film_short_detail.imdb_rating,
            ),
        )

    async def search_by_director(self, search_query: str):
        # TODO не будет работать
        film_short_detail = await self.movie_repository.find_movie_by_name(search_query)
        film_detail = await self.movie_repository.find_movie_by_id(film_short_detail.film_id)
        return AssistantResponse(
            text=choice(Message.FIND_BY_DIRECTOR_MESSAGE_LIST.value).format(
                film=film_detail.title,
                director=search_query,
            ),
        )

    async def not_recognized(self):
        # TODO доделать ответы
        return AssistantResponse(
            text="не понял",
        )

    async def dispatch_intent(self, assistant_request: AssistantRequest) -> AssistantResponse:
        """Выбор нужного обработчика по интенту."""
        match assistant_request.intent:
            case IntentChoice.FILM_ACTORS:
                response = await self.get_film_actors(assistant_request.search_value)
            case IntentChoice.FILM_DESCRIPTION:
                response = await self.get_film_description(assistant_request.search_value)
            case IntentChoice.FILM_DIRECTORS:
                response = await self.get_film_directors(assistant_request.search_value)
            case IntentChoice.SEARCH_BY_DIRECTOR:
                response = await self.search_by_director(assistant_request.search_value)
            case IntentChoice.FILM_RATING:
                response = await self.get_film_rating(assistant_request.search_value)
            case _:
                response = await self.not_recognized()

        return response
