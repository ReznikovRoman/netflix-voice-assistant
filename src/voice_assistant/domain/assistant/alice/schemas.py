from pydantic import Field, validator

from voice_assistant.common.schemas import BaseOrjsonSchema

from ..schemas import AssistantRequest, AssistantResponse, IntentChoice


class NluField(BaseOrjsonSchema):
    """Поле `nlu` в запросе от Яндекс.Диалогов."""

    tokens: list | None = Field(default_factory=list)
    entities: list | None = Field(default_factory=list)
    intents: dict[IntentChoice, dict] = {}

    @validator("intents", pre=True)
    def remove_redundant_intents(cls, value: dict[str, dict]) -> dict[IntentChoice, dict]:
        """Убирает лишние интенты из запроса от Яндекс.Диалогов."""
        for key in list(value.keys()):
            try:
                _ = IntentChoice(key)
            except ValueError:
                del value[key]
        return value


class RequestField(BaseOrjsonSchema):
    """Поле `request` в запросе от Яндекс.Диалогов."""

    command: str
    original_utterance: str
    nlu: NluField | None = {}


class AliceRequest(AssistantRequest):
    """Запрос от Яндекс.Диалогов."""

    meta: dict
    request: RequestField
    session: dict
    version: str
    state: dict | None = {}


class AliceResponse(AssistantResponse):
    """Ответ для Яндекс.Диалогов."""

    response: dict
    version: str
    session_state: dict | None = {}
