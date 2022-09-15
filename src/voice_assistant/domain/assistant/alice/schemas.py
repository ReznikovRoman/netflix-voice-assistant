import enum

from pydantic import Field

from voice_assistant.common.schemas import BaseOrjsonSchema

from ..types import AssistantRequest, AssistantResponse

# TODO: добавить аннотации TypedDict для сущностей Яндекс.Диалогов
#  - meta, session, version, response


class IntentChoice(str, enum.Enum):
    """Список намерений в Яндекс.Диалогах."""

    FIND_FILM = "find_film"
    FILM_ACTORS = "actors_in_the_film"
    FILM_DIRECTORS = "film_director"
    FILM_DURATION = "movie_duration"


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


class AliceResponse(AssistantResponse):
    """Ответ для Яндекс.Диалогов."""

    meta: dict
    response: dict
    session: dict
    version: str
