from ..services import AssistantService


class AliceService(AssistantService):
    """Голосовой ассистент на основе Алисы."""

    def process_request(self):
        return {"message": "alice"}
