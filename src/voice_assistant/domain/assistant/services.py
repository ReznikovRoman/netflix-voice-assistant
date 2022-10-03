import abc

from dependency_injector.errors import NoSuchProviderError
from dependency_injector.providers import Factory

from .exceptions import UnknownAssistantProvider
from .schemas import AssistantRequest, AssistantResponse


class BaseAssistantService(abc.ABC):
    """Base voice assistant service."""

    @abc.abstractmethod
    async def process_request(self, request: AssistantRequest, /) -> AssistantResponse:
        """Process provider request."""

    @abc.abstractmethod
    def build_request_from_provider_data(self, data: dict, /) -> AssistantRequest:
        """Transform data from provider request to a domain object (provider-specific request)."""


def get_assistant_service(
    assistant_service_factory: Factory[BaseAssistantService], *, provider: str,
) -> BaseAssistantService:
    """Get a provider-specific service class by slug."""
    try:
        return assistant_service_factory(provider)
    except NoSuchProviderError:
        raise UnknownAssistantProvider()
