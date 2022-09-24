import uuid

from pydantic import BaseModel

from voice_assistant.common.schemas import BaseOrjsonSchema
from voice_assistant.domain.assistant.enums import IntentChoice


class AssistantRequest(BaseOrjsonSchema):
    """Базовый класс запроса от провайдера."""

    intent: IntentChoice = IntentChoice.NOT_RECOGNIZED
    search_value: str | None = None


class AssistantResponse(BaseOrjsonSchema):
    """Базовый класс ответа для провайдера."""

    text: str


class FilmShortDetail(BaseModel):
    """Сокращенная модель для запроса фильма (по имени)."""

    title: str
    film_id: uuid.UUID
    imdb_rating: float | None


class FilmFullDetail(FilmShortDetail):
    """Модель для запроса полной информации о фильме (по id)."""

    description: str
    actors: str
    directors: str


class PersonShortDetail(BaseModel):
    """Список персон."""

    full_name: str
    person_id: uuid.UUID


class FilmList(BaseModel):
    """Список фильмов в формате строки."""

    films: str
