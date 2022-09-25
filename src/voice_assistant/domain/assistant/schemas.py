import uuid

from pydantic import BaseModel

from voice_assistant.common.schemas import BaseOrjsonSchema
from voice_assistant.domain.assistant.enums import IntentChoice


class AssistantRequest(BaseOrjsonSchema):
    """Базовый класс запроса от провайдера."""

    intent: IntentChoice = IntentChoice.NOT_RECOGNIZED
    search_query: str | None = None  # TODO: возможно можно сделать поле обязательным


class AssistantResponse(BaseOrjsonSchema):
    """Базовый класс ответа для провайдера."""

    text: str


class FilmShortDetail(BaseModel):
    """Короткая информация о фильме."""

    film_id: uuid.UUID
    title: str
    imdb_rating: float | None = None


class FilmFullDetail(BaseModel):
    """Полная информация о фильме."""

    film_id: uuid.UUID
    title: str
    imdb_rating: float | None = None
    description: str
    actors: str
    directors: str


class PersonShortDetail(BaseModel):
    """Короткая информация о персоне."""

    person_id: uuid.UUID
    full_name: str


class FilmList(BaseModel):
    """Список фильмов в формате строки."""

    films: str
