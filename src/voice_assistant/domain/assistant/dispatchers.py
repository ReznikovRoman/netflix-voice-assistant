from random import choice

from dependency_injector.providers import Factory

from .enums import AssistantProviderSlug
from .exceptions import UnknownAssistantProvider
from .messages import Message
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
    def dispatcher_intent(self, assistant_request: AssistantRequest) -> AssistantResponse:
        """Выбор нужного обработчика, по интенту."""
        # TODO добавить работу с репозиторием
        match assistant_request.intent:
            case IntentChoice.FILM_ACTORS:
                response = AssistantResponse(
                    text=choice(
                        Message.ACTORS_IN_FILM_MESSAGE_LIST).format(assistant_request.search_value, "Brad Pit",
                                                                    ),
                )
                return response

            case IntentChoice.FILM_DESCRIPTION:
                response = AssistantResponse(
                    text=choice(
                        Message.FIND_FILM_MESSAGE_LIST).format(assistant_request.search_value, "description",
                                                               ),
                )
                return response

            case IntentChoice.FILM_DIRECTORS:
                response = AssistantResponse(
                    text=choice(
                        Message.FILM_DIRECTOR_MESSAGE_LIST).format(assistant_request.search_value, "Torantino",
                                                                   ),
                )
                return response

            case IntentChoice.SEARCH_BY_DIRECTOR:
                response = AssistantResponse(
                    text=choice(
                        Message.FIND_BY_DIRECTOR_MESSAGE_LIST).format(assistant_request.search_value, "tor, Мстители",
                                                                      ),
                )
                return response

            case IntentChoice.FILM_DURATION:
                response = AssistantResponse(
                    text=choice(
                        Message.FILM_DURATION_MESSAGE_LIST).format(assistant_request.search_value, "01:30",
                                                                   ),
                )
                return response

            case _:
                response = AssistantResponse(
                    text=choice(
                        Message.FIND_FILM_MESSAGE_LIST).format(assistant_request.search_value, "description",
                                                               ),
                )
                return response
