from .schemas import AliceRequest, AliceResponse


class AliceService:
    """Голосовой ассистент на основе Алисы."""

    def build_request_from_raw_data(self, meta, session, version, response):
        """Построение ответа для Яндекс.Диалогов."""
        alice_response_model = AliceResponse(
            meta=meta,
            session=session,
            version=version,
            response=response,
        )
        return alice_response_model

    def process_request(self, context: AliceRequest) -> AliceResponse:
        """Обработчик запросов с Яндекс.Диалогов."""
        answer = "Hi! I`m bot"
        response = self.build_request_from_raw_data(
            AliceRequest.meta,
            AliceRequest.session,
            AliceRequest.version,
            response={
                "text": answer,
                "end_session": False,
            },
        )
        return response
