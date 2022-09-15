from dependency_injector.providers import Factory

from .enums import AssistantProviderSlug
from .exceptions import UnknownAssistantProvider
from .schemas import AssistantResponse
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
