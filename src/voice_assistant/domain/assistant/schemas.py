import uuid

from pydantic import BaseModel

from voice_assistant.common.schemas import BaseOrjsonSchema
from voice_assistant.domain.assistant.enums import IntentChoice


class AssistantRequest(BaseOrjsonSchema):
    """Базовый класс запроса от провайдера."""

    intent: IntentChoice | None = None
    search_value: str | None = None


class AssistantResponse(BaseOrjsonSchema):
    """Базовый класс ответа для провайдера."""

    text: str


class FilmByName(BaseModel):
    title: str
    film_id: uuid.UUID


class FilmDetail(BaseModel):
    title: str
    imdb_rating: float | None
    description: str
    actors: str
    directors: str
