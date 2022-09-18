import enum

from pydantic import Field

from voice_assistant.common.schemas import BaseOrjsonSchema


class IntentChoice(str, enum.Enum):
    """Список намерений пользователя."""

    FILM_DESCRIPTION = "film_description"
    FILM_ACTORS = "actors_in_the_film"
    FILM_DIRECTORS = "film_director"
    FILM_DURATION = "movie_duration"


class AssistantRequest(BaseOrjsonSchema):
    """Базовый класс запроса от провайдера."""

    intent: IntentChoice | None = Field(default_factory=None)
    search_value: str | None = Field(default_factory=None)


class AssistantResponse(BaseOrjsonSchema):
    """Базовый класс ответа для провайдера."""

    text: str | dict = Field(default_factory=str)
