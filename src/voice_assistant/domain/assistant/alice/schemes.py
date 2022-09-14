from typing import Union

from pydantic import BaseModel


class SearchByDirector(BaseModel):
    """Интент для поиска фильма по режиссеру."""

    intent_name: str = 'search_by_director'
    search_by_director: dict


class ActorsInTheFilm(BaseModel):
    """Интент для поиска фильмов в котором снимался актер."""

    intent_name: str = 'actors_in_the_film'
    actors_in_the_film: dict


class FilmDirector(BaseModel):
    """Интент для получения режиссера фильма."""

    intent_name: str = 'film_director'
    film_director: dict


class MovieDuration(BaseModel):
    """Интент для получения длительности фильма."""

    intent_name: str = 'movie_duration'
    movie_duration: dict


class FindFilm(BaseModel):
    """Интент для поиска фильма в базе."""

    intent_name: str = 'find_film'
    find_film: dict


class EmptyIntent(BaseModel):
    """Пустой интент.
        Приходит в случае если запрос не попал ни в один
        из выше перечисленных.
    """
    intent_name: str = 'empty'


class Nlu(BaseModel):
    """Поле nlu в запросе от Яндекс диалогов"""
    tokens: list
    intents: Union[FilmDirector, FindFilm, ActorsInTheFilm, SearchByDirector, MovieDuration, EmptyIntent]


class RequestField(BaseModel):
    """Поле request в запросе от Яндекс диалогов"""
    command: str
    original_utterance: str
    nlu: Nlu


class AliceRequest(BaseModel):
    """запрос от Яндекс диалогов."""
    meta: dict
    request: RequestField
    session: dict
    version: str


class AliceResponse(BaseModel):
    """ответ для Яндекс диалогов."""
    meta: dict
    response: dict
    session: dict
    version: str
