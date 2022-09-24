from .. import IntentDispatcher
from ..enums import IntentChoice, Message
from ..schemas import AssistantRequest
from ..services import AssistantService
from .schemas import AliceRequest, AliceResponse


class AliceService(AssistantService):
    """Голосовой ассистент на основе Алисы."""

    def __init__(self, intent_dispatcher: IntentDispatcher) -> None:
        self.intent_dispatcher = intent_dispatcher

    async def process_request(self, request: AliceRequest, /) -> AliceResponse:
        """Процесс обработки запросов от Алисы."""
        # первичный запрос (всегда приветственный/ознакомительный)
        if not request.request.command:
            return await self._build_response(
                version=request.version,
                response={
                    "text": Message.WELCOME_HELP_MESSAGE.value,
                    "end_session": False,
                },
                assistant_request=None,
            )
        intent = IntentChoice.NOT_RECOGNIZED.value
        search_query = request.state.get("session").get("search_value")
        # если есть поисковый запрос
        if request.request.nlu.intents:
            intent = list(request.request.nlu.intents.keys())[0].value  # TODO Как то кривовато вышло
            if request.request.nlu.intents.get(intent).get("slots"):
                # если есть поисковое значение
                search_query = request.request.nlu.intents.get(intent).get("slots").get("search_value").get("value")

        assistant_request = AssistantRequest(
            intent=intent,
            search_query=search_query,
        )
        assistant_response = await self.intent_dispatcher.dispatch_intent(assistant_request)

        return await self._build_response(
            version=request.version,
            response={
                "text": assistant_response.text,
                "end_session": False,
            },
            assistant_request=assistant_request,
        )

    async def build_request_from_provider_data(self, data: dict, /) -> AliceRequest:
        return AliceRequest(**data)

    @staticmethod
    async def _build_response(
        *,
        assistant_request: AssistantRequest = None,
        version: str,
        response: dict,
    ) -> AliceResponse:
        """Построение ответа для Яндекс.Диалогов."""
        alice_response_model = AliceResponse(
            version=version,
            response=response,
            session_state=assistant_request,
        )
        return alice_response_model
