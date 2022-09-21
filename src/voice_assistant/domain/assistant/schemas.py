from voice_assistant.common.schemas import BaseOrjsonSchema
from voice_assistant.domain.assistant.enums import IntentChoice


class AssistantRequest(BaseOrjsonSchema):
    """Базовый класс запроса от провайдера."""

    intent: IntentChoice | None = None
    search_value: str | None = None


class AssistantResponse(BaseOrjsonSchema):
    """Базовый класс ответа для провайдера."""

    text: str
