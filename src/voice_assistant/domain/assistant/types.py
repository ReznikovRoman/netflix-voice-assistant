from voice_assistant.common.schemas import BaseOrjsonSchema


class AssistantRequest(BaseOrjsonSchema):
    """Базовый класс запроса от провайдера."""


class AssistantResponse(BaseOrjsonSchema):
    """Базовый класс ответа для провайдера."""
