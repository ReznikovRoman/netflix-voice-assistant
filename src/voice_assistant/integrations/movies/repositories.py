import uuid

from ...domain.assistant.schemas import FilmByName, FilmDetail
from .clients import MovieClient
from .types import QueryOptions


class MovieRepository:
    """Репозиторий для работы с данными из сервиса Netflix Movies."""

    def __init__(self, movie_client: MovieClient) -> None:
        assert isinstance(movie_client, MovieClient)
        self._movie_client = movie_client

    async def find_movie_by_name(self, name: str, /) -> FilmByName:
        """Поиск фильмов по названию."""
        query_options = QueryOptions()
        query_options.page_number_pagination.page_size = 0
        film = await self._movie_client.search_films(name, options=query_options)
        return FilmByName(film_id=film[0].uuid, title=film[0].title)

    async def find_movie_by_id(self, film_id: uuid, /) -> FilmDetail:
        """Поиск фильмов по id."""
        film_by_id = await self._movie_client.get_film_by_id(film_id)
        return FilmDetail(
            title=film_by_id.title,
            imdb_rating=film_by_id.imdb_rating,
            description=film_by_id.description,
            actors=" ".join([actors.full_name for actors in film_by_id.actors]),
            directors=" ".join([directors.full_name for directors in film_by_id.directors]),
        )
