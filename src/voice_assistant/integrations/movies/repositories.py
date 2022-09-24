import uuid

from src.voice_assistant.domain.assistant.schemas import FilmFullDetail, FilmShortDetail

from .clients import MovieClient
from .types import QueryOptions
from .types.api import PageNumberPaginationOptions


class MovieRepository:
    """Репозиторий для работы с данными из сервиса Netflix Movies."""

    def __init__(self, movie_client: MovieClient) -> None:
        assert isinstance(movie_client, MovieClient)
        self._movie_client = movie_client

    async def find_movie_by_name(self, name: str, /) -> FilmShortDetail:
        """Поиск фильмов по названию."""
        pagination_options = PageNumberPaginationOptions()
        pagination_options.page_size = 1
        pagination_options.page_number = 1

        query_options = QueryOptions()
        query_options.page_number_pagination = pagination_options

        films = await self._movie_client.search_films(name, options=query_options)
        return FilmShortDetail(film_id=films[0].uuid, title=films[0].title, imdb_rating=films[0].imdb_rating)

    async def find_movie_by_id(self, film_id: uuid, /) -> FilmFullDetail:
        """Поиск фильмов по id."""
        film = await self._movie_client.get_film_by_id(film_id)
        return FilmFullDetail(
            title=film.title,
            imdb_rating=film.imdb_rating,
            description=film.description,
            actors=" ".join([actors.full_name for actors in film.actors]),
            directors=" ".join([directors.full_name for directors in film.directors]),
        )
