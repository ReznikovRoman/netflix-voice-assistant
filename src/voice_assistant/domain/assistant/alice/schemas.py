from pydantic import Field, validator

from voice_assistant.common.schemas import BaseOrjsonSchema

from ..schemas import AssistantRequest, AssistantResponse, IntentChoice


class NluField(BaseOrjsonSchema):
    """Field `nlu` in a Yandex.Dialogs request."""

    tokens: list | None = Field(default_factory=list)
    entities: list | None = Field(default_factory=list)
    intents: dict[IntentChoice, dict] = {}

    @validator("intents", pre=True)
    def remove_redundant_intents(cls, value: dict[str, dict]) -> dict[IntentChoice, dict]:
        """Remove redundant intents from Yandex.Dialog request."""
        for key in list(value.keys()):
            try:
                _ = IntentChoice(key)
            except ValueError:
                del value[key]
        return value


class RequestField(BaseOrjsonSchema):
    """Field `request` in a Yandex.Dialogs request."""

    command: str
    original_utterance: str
    nlu: NluField | None = {}


class AliceRequest(AssistantRequest):
    """Request from Yandex.Dialogs."""

    meta: dict
    request: RequestField
    session: dict
    version: str
    state: dict | None = {}


class AliceResponse(AssistantResponse):
    """Response for Yandex.Dialogs."""

    response: dict
    version: str
    session_state: dict | None = {}
