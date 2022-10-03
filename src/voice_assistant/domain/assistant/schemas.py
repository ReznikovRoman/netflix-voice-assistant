import uuid

from pydantic import BaseModel

from voice_assistant.common.schemas import BaseOrjsonSchema
from voice_assistant.domain.assistant.enums import IntentChoice


class AssistantRequest(BaseOrjsonSchema):
    """Base assistant request from provider."""

    intent: IntentChoice = IntentChoice.NOT_RECOGNIZED
    search_query: str | None = None


class AssistantResponse(BaseOrjsonSchema):
    """Base assistant response for provider."""

    text: str


class FilmShortDetail(BaseModel):
    """Film short details."""

    film_id: uuid.UUID
    title: str
    imdb_rating: float | None = None


class FilmFullDetail(BaseModel):
    """Film full details."""

    film_id: uuid.UUID
    title: str
    imdb_rating: float | None = None
    description: str
    actors: str
    directors: str


class PersonShortDetail(BaseModel):
    """Person short details."""

    person_id: uuid.UUID
    full_name: str


class FilmList(BaseModel):
    """Film list, comma-separated."""

    films: str
