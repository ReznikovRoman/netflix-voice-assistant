from ..dispatchers import IntentDispatcher
from ..enums import DefaultResponseMessage, IntentChoice
from ..schemas import AssistantRequest
from ..services import BaseAssistantService
from .schemas import AliceRequest, AliceResponse


class AliceService(BaseAssistantService):
    """Voice assistant based on Yandex.Dialogs."""

    def __init__(self, intent_dispatcher: IntentDispatcher) -> None:
        assert isinstance(intent_dispatcher, IntentDispatcher)
        self._intent_dispatcher = intent_dispatcher

    async def process_request(self, request: AliceRequest, /) -> AliceResponse:
        """Process request from Yandex.Dialogs."""
        if not request.request.command:  # first ("welcome") request
            response_text = DefaultResponseMessage.WELCOME_HELP_MESSAGE
            return self._build_response(
                text=response_text,
                version=request.version,
                response={
                    "text": response_text,
                    "end_session": False,
                },
                session_state={},
            )
        assistant_request = self._build_assistant_request_from_provider(request)
        assistant_response = await self._intent_dispatcher.dispatch_intent_by_request(assistant_request)
        response_text = assistant_response.text
        return self._build_response(
            text=response_text,
            version=request.version,
            response={
                "text": response_text,
                "end_session": False,
            },
            session_state=assistant_request.dict(),
        )

    def build_request_from_provider_data(self, data: dict, /) -> AliceRequest:
        return AliceRequest(**data)

    @staticmethod
    def _build_response(*, text: str, version: str, response: dict, session_state: dict) -> AliceResponse:
        """Build response for Yandex.Dialogs."""
        return AliceResponse(text=text, version=version, response=response, session_state=session_state)

    @staticmethod
    def _build_assistant_request_from_provider(alice_request: AliceRequest, /) -> AssistantRequest:
        """Build base request by provider data."""
        intent = IntentChoice.NOT_RECOGNIZED
        search_query = alice_request.state.get("session").get("search_query")
        if alice_request.request.nlu.intents:  # if there is a search query
            intent = list(alice_request.request.nlu.intents.keys())[0]
            search_query = (
                alice_request.request.nlu.intents.get(intent, {})
                .get("slots", {})
                .get("search_query", {}).get("value", alice_request.state.get("session").get("search_query"))
            )
            if search_query is None:
                intent = IntentChoice.MISSING_SEARCH_QUERY
        return AssistantRequest(intent=intent, search_query=search_query)
