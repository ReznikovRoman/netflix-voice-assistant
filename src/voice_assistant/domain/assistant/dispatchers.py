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
                response = await assistant_service.process_request(provider_request)
            case _:
                raise UnknownAssistantProvider()
        return response


class IntentDispatcher:
    """Диспатчер интентов."""

    def __init__(self, movie_repository: MovieRepository) -> None:
        self.movie_repository = movie_repository

    async def get_film_description(self, search_query: str):
        film_short_detail = await self.movie_repository.find_movie_by_name(search_query)
        if not film_short_detail:
            return await self.not_found(search_query)
        film_detail = await self.movie_repository.find_movie_by_id(film_short_detail.film_id)
        return AssistantResponse(
            text=choice(Message.FILM_DESCRIPTION_MESSAGE_LIST.value).format(
                film=search_query,
                description=film_detail.description,
            ),
        )

    async def get_film_actors(self, search_query: str):
        film_short_detail = await self.movie_repository.find_movie_by_name(search_query)
        if not film_short_detail:
            return await self.not_found(search_query)
        film_detail = await self.movie_repository.find_movie_by_id(film_short_detail.film_id)
        return AssistantResponse(
            text=choice(Message.ACTORS_IN_FILM_MESSAGE_LIST.value).format(
                film=search_query,
                actors=film_detail.actors,
            ),
        )

    async def get_film_directors(self, search_query: str):
        film_short_detail = await self.movie_repository.find_movie_by_name(search_query)
        if not film_short_detail:
            return await self.not_found(search_query)
        film_detail = await self.movie_repository.find_movie_by_id(film_short_detail.film_id)
        return AssistantResponse(
            text=choice(Message.FILM_DIRECTOR_MESSAGE_LIST.value).format(
                film=search_query,
                director=film_detail.directors,
            ),
        )

    async def get_film_rating(self, search_query: str):
        film_short_detail = await self.movie_repository.find_movie_by_name(search_query)
        if not film_short_detail:
            return await self.not_found(search_query)
        return AssistantResponse(
            text=choice(Message.FILM_RATING_MESSAGE_LIST.value).format(
                film=search_query,
                rating=film_short_detail.imdb_rating,
            ),
        )

    async def search_by_director(self, search_query: str):
        person_short_detail = await self.movie_repository.find_person_by_name(search_query)
        if not person_short_detail:
            return await self.not_found(search_query)
        films = await self.movie_repository.find_film_by_person_id(person_short_detail.person_id)
        return AssistantResponse(
            text=choice(Message.FIND_BY_DIRECTOR_MESSAGE_LIST.value).format(
                films=films,
                director=search_query,
            ),
        )

    async def help(self):
        return AssistantResponse(text=Message.HELP.value)

    async def not_recognized(self):
        return AssistantResponse(text=Message.INTENT_NOT_FOUND.value)

    async def not_found(self, search_query: str):
        return AssistantResponse(
            text=Message.NOT_FOUND_MESSAGE_TEMPLATE.value.format(search_query=search_query),
        )

    async def exception_answer(self):
        return AssistantResponse(text=Message.ERROR_MESSAGE.value)

    async def dispatch_intent(self, assistant_request: AssistantRequest) -> AssistantResponse:
        """Выбор нужного обработчика по интенту."""
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
                response = await self.not_recognized()
            case IntentChoice.HELP:
                response = await self.help()
            case _:
                response = await self.exception_answer()

        return response
