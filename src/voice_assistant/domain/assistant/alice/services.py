from .. import IntentDispatcher
from ..messages import Message
from ..schemas import AssistantRequest
from ..services import AssistantService
from .schemas import AliceRequest, AliceResponse


class AliceService(AssistantService):
    """Голосовой ассистент на основе Алисы."""

    def __init__(self, intent_service: IntentDispatcher) -> None:
        self.intent_service = intent_service

    def process_request(self, request: AliceRequest, /) -> AliceResponse:
        """Процесс обработки запросов от Алисы."""
        # первичный запрос (всегда приветственный/ознакомительный)
        if not request.request.command:
            return self._build_response(
                version=request.version,
                response={
                    "text": Message.WELCOME_MESSAGE,
                    "end_session": False,
                },
                session_state=None,
            )
        intent = None
        value = None
        # если есть поисковый запрос
        if request.request.nlu.intents:
            intent = list(request.request.nlu.intents.keys())[0].value  # TODO Как то кривовато вышло
            if request.request.nlu.intents.get(intent).get("slots"):
                # если есть поисковое значение
                value = request.request.nlu.intents.get(intent).get("slots").get("movie_name").get("value")
            else:
                # если нет пробую взять из state сессии
                state = AssistantRequest(**request.state.get("session"))
                value = state.search_value

        assistant_request = AssistantRequest(
            intent=intent,
            search_value=value,
        )
        assistant_response = self.intent_service.dispatcher_intent(assistant_request)

        return self._build_response(
            version=request.version,
            response={
                "text": assistant_response.text,
                "end_session": False,
            },
            session_state=assistant_request,
        )

    def build_request_from_provider_data(self, data: dict, /) -> AliceRequest:
        return AliceRequest(**data)

    @staticmethod
    def _build_response(*, version: str, response: dict, session_state: AssistantRequest | None) -> AliceResponse:
        """Построение ответа для Яндекс.Диалогов."""
        alice_response_model = AliceResponse(
            version=version,
            response=response,
            session_state=session_state,
        )
        return alice_response_model
