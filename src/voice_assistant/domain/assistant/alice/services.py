from ..services import AssistantService
from .schemas import AliceRequest, AliceResponse


class AliceService(AssistantService):
    """Голосовой ассистент на основе Алисы."""

    def process_request(self, request: AliceRequest, /) -> AliceResponse:
        answer = "Hi! I`m bot"
        response = self._build_response(
            meta=AliceRequest.meta, session=AliceRequest.session, version=AliceRequest.version,
            response={
                "text": answer,
                "end_session": False,
            },
        )
        return response

    def build_request_from_provider_data(self, data: dict, /) -> AliceRequest:
        return AliceRequest(**data)

    @staticmethod
    def _build_response(*, meta: dict, session: dict, version: str, response: dict) -> AliceResponse:
        """Построение ответа для Яндекс.Диалогов."""
        alice_response_model = AliceResponse(meta=meta, session=session, version=version, response=response)
        return alice_response_model
