import uuid

from voice_assistant.domain.assistant.schemas import FilmFullDetail, FilmList, FilmShortDetail, PersonShortDetail

from .clients import MovieClient
from .types import QueryOptions
from .types.api import PageNumberPaginationOptions


class MovieRepository:
    """Репозиторий для работы с данными из сервиса Netflix Movies."""

    def __init__(self, movie_client: MovieClient) -> None:
        assert isinstance(movie_client, MovieClient)
        self._movie_client = movie_client

    async def find_movie_by_name(self, name: str, /) -> FilmShortDetail | None:
        """Поиск фильмов по названию."""
        films = await self._movie_client.search_films(
            name,
            options=self._create_query_options(page_size=1, page_number=1),
        )
        if not films:
            return None
        return FilmShortDetail(
            film_id=films[0].uuid,
            title=films[0].title,
            imdb_rating=films[0].imdb_rating,
        )

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

    async def find_person_by_name(self, person_name: str, /) -> PersonShortDetail | None:
        """Поиск по person_name."""
        person = await self._movie_client.search_persons(
            person_name,
            options=self._create_query_options(page_size=1, page_number=1),
        )
        if not person:
            return None
        return PersonShortDetail(
            person_id=person[0].uuid,
            full_name=person[0].full_name,
        )

    async def find_film_by_person_id(self, person_id: uuid, /) -> FilmList:
        """Поиск фильмов с участием person_id."""
        films = await self._movie_client.get_person_films(person_id)
        return FilmList(" ".join([film.title for film in films]))

    @staticmethod
    def _create_query_options(page_size: int, page_number: int) -> QueryOptions:
        pagination_options = PageNumberPaginationOptions(page_size=page_size, page_number=page_number)
        return QueryOptions(page_number_pagination=pagination_options)
