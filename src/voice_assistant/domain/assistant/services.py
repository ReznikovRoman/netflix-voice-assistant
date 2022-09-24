import abc

from dependency_injector.errors import NoSuchProviderError
from dependency_injector.providers import Factory

from .exceptions import UnknownAssistantProvider
from .schemas import AssistantRequest, AssistantResponse


class AssistantService(abc.ABC):
    """Базовый сервис голосового ассистента."""

    @abc.abstractmethod
    async def process_request(self, request: AssistantRequest, /) -> AssistantResponse:
        """Обработка запроса пользователя."""

    @abc.abstractmethod
    async def build_request_from_provider_data(self, data: dict, /) -> AssistantRequest:
        """Преобразование данных от провайдера в доменный объект."""


def get_assistant_service(assistant_service_factory: Factory[AssistantService], *, provider: str) -> AssistantService:
    """Получение класса для работы с провайдером по названию."""
    try:
        return assistant_service_factory(provider)
    except NoSuchProviderError:
        raise UnknownAssistantProvider()
