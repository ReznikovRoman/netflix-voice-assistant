import abc

from dependency_injector.errors import NoSuchProviderError
from dependency_injector.providers import Factory

from .exceptions import UnknownAssistantProvider


class AssistantService(abc.ABC):
    """Базовый сервис голосового ассистента."""

    @abc.abstractmethod
    def process_request(self, context):
        """Обработка запроса пользователя."""


def get_assistant_service(assistant_service_factory: Factory[AssistantService], *, provider: str) -> AssistantService:
    """Получение класса для работы с провайдером по названию."""
    try:
        return assistant_service_factory(provider)
    except NoSuchProviderError:
        raise UnknownAssistantProvider()
