import enum

from orjson import orjson
from pydantic import BaseModel


def orjson_dumps(value, *, default):
    return orjson.dumps(value, default=default).decode()


class BaseOrjsonSchema(BaseModel):
    """Базовая схема ответа с orjson."""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class IntentsEnum(enum.Enum):
    find_film = "find_film"
    actors_in_the_film = "actors_in_the_film"
    film_director = "film_director"
    movie_duration = "movie_duration"


class Nlu(BaseModel):
    """Поле nlu в запросе от Яндекс.Диалогов."""

    tokens: list
    intents: dict[IntentsEnum, dict] | None


class RequestField(BaseModel):
    """Поле request в запросе от Яндекс.Диалогов."""

    command: str
    original_utterance: str
    nlu: Nlu


class AliceRequest(BaseOrjsonSchema):
    """Запрос от Яндекс.Диалогов."""

    meta: dict
    request: RequestField
    session: dict
    version: str


class AliceResponse(BaseOrjsonSchema):
    """Ответ для Яндекс.Диалогов."""

    meta: dict
    response: dict
    session: dict
    version: str
