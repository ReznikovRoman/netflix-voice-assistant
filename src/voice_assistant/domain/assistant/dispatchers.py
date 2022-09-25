import random

from dependency_injector.providers import Factory

from voice_assistant.integrations.movies import MovieRepository

from .enums import AssistantProviderSlug, DefaultResponseMessage, ResponseMessageTemplate
from .exceptions import FilmNotFoundError, UnknownAssistantProvider
from .schemas import AssistantRequest, AssistantResponse, FilmFullDetail, IntentChoice
from .services import AssistantService, get_assistant_service


class AssistantProviderDispatcher:
    """Диспатчер провайдеров голосового помощника."""

    def __init__(self, assistant_service_factory: Factory[AssistantService]) -> None:
        self._assistant_service_factory = assistant_service_factory

    async def dispatch_provider(self, provider: AssistantProviderSlug, /, *, data: dict) -> AssistantResponse:
        """Выбор корректного сервиса для данного провайдера голосового ассистента."""
        assistant_service = get_assistant_service(self._assistant_service_factory, provider=provider)
        provider_request = assistant_service.build_request_from_provider_data(data)
        match provider:
            case AssistantProviderSlug.YANDEX_ALICE:
                response = await assistant_service.process_request(provider_request)
            case _:
                raise UnknownAssistantProvider()
        return response


class IntentDispatcher:
    """Диспатчер интентов."""

    def __init__(self, movie_repository: MovieRepository) -> None:
        assert isinstance(movie_repository, MovieRepository)
        self._movie_repository = movie_repository

    async def dispatch_intent_by_request(self, assistant_request: AssistantRequest, /) -> AssistantResponse:
        """Выбор нужного ответа пользователю на основе интента."""
        match assistant_request.intent:
            case IntentChoice.FILM_ACTORS:
                response = await self.get_film_actors(assistant_request.search_query)
            case IntentChoice.FILM_DESCRIPTION:
                response = await self.get_film_description(assistant_request.search_query)
            case IntentChoice.FILM_DIRECTORS:
                response = await self.get_film_directors(assistant_request.search_query)
            case IntentChoice.SEARCH_BY_DIRECTOR:
                response = await self.search_by_director(assistant_request.search_query)
            case IntentChoice.FILM_RATING:
                response = await self.get_film_rating(assistant_request.search_query)
            case IntentChoice.NOT_RECOGNIZED:
                response = AssistantResponse(text=DefaultResponseMessage.INTENT_NOT_FOUND)
            case IntentChoice.HELP:
                response = AssistantResponse(text=DefaultResponseMessage.HELP)
            case _:
                response = AssistantResponse(text=DefaultResponseMessage.ERROR_MESSAGE)
        return response

    async def get_film_description(self, search_query: str, /) -> AssistantResponse:
        try:
            film_detail = await self._get_film_by_name(search_query)
        except FilmNotFoundError:
            return await self._get_not_found_response(search_query=search_query)
        return AssistantResponse(
            text=random.choice(ResponseMessageTemplate.FILM_DESCRIPTION_MESSAGE_LIST).format(
                film=search_query,
                description=film_detail.description,
            ),
        )

    async def get_film_actors(self, search_query: str, /) -> AssistantResponse:
        try:
            film_detail = await self._get_film_by_name(search_query)
        except FilmNotFoundError:
            return await self._get_not_found_response(search_query=search_query)
        return AssistantResponse(
            text=random.choice(ResponseMessageTemplate.ACTORS_IN_FILM_MESSAGE_LIST).format(
                film=search_query,
                actors=film_detail.actors,
            ),
        )

    async def get_film_directors(self, search_query: str, /) -> AssistantResponse:
        try:
            film_detail = await self._get_film_by_name(search_query)
        except FilmNotFoundError:
            return await self._get_not_found_response(search_query=search_query)
        return AssistantResponse(
            text=random.choice(ResponseMessageTemplate.FILM_DIRECTOR_MESSAGE_LIST).format(
                film=search_query,
                director=film_detail.directors,
            ),
        )

    async def get_film_rating(self, search_query: str, /) -> AssistantResponse:
        film = await self._movie_repository.find_movie_by_name(search_query)
        if film is None:
            return await self._get_not_found_response(search_query=search_query)
        return AssistantResponse(
            text=random.choice(ResponseMessageTemplate.FILM_RATING_MESSAGE_LIST).format(
                film=search_query,
                rating=film.imdb_rating,
            ),
        )

    async def search_by_director(self, search_query: str, /) -> AssistantResponse:
        person = await self._movie_repository.find_person_by_name(search_query)
        if person is None:
            return await self._get_not_found_response(search_query=search_query)
        films = await self._movie_repository.get_person_films(person.person_id)
        return AssistantResponse(
            text=random.choice(ResponseMessageTemplate.FIND_BY_DIRECTOR_MESSAGE_LIST).format(
                films=films.films,
                director=search_query.title(),
            ),
        )

    async def _get_film_by_name(self, name: str, /) -> FilmFullDetail:
        film_short_detail = await self._movie_repository.find_movie_by_name(name)
        if film_short_detail is None:
            raise FilmNotFoundError
        return await self._movie_repository.get_movie_by_id(film_short_detail.film_id)

    @staticmethod
    async def _get_not_found_response(*, search_query: str) -> AssistantResponse:
        return AssistantResponse(
            text=DefaultResponseMessage.NOT_FOUND_MESSAGE_TEMPLATE.format(search_query=search_query))
