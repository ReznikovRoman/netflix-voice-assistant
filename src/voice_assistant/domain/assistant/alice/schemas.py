from pydantic import Field

from voice_assistant.common.schemas import BaseOrjsonSchema

from ..schemas import AssistantRequest, AssistantResponse, IntentChoice

# TODO: добавить аннотации TypedDict для сущностей Яндекс.Диалогов
#  - meta, session, version, response


class NluField(BaseOrjsonSchema):
    """Поле `nlu` в запросе от Яндекс.Диалогов."""

    tokens: list | None = Field(default_factory=list)
    entities: list | None = Field(default_factory=list)
    intents: dict[IntentChoice, dict] = Field(default_factory=dict)


class RequestField(BaseOrjsonSchema):
    """Поле `request` в запросе от Яндекс.Диалогов."""

    command: str
    original_utterance: str
    nlu: NluField | None = Field(default_factory=dict)


class AliceRequest(AssistantRequest):
    """Запрос от Яндекс.Диалогов."""

    meta: dict
    request: RequestField
    session: dict
    version: str
    state: dict | None = Field(default_factory=dict)


class AliceResponse(AssistantResponse):
    """Ответ для Яндекс.Диалогов."""

    response: dict
    version: str
    session_state: dict | None = None
