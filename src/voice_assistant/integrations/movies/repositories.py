import uuid

from netflix.movies.client import AsyncMovieClient
from netflix.movies.client.types import QueryOptions
from netflix.movies.client.types.api import PageNumberPaginationOptions

from voice_assistant.domain.assistant.schemas import FilmFullDetail, FilmList, FilmShortDetail, PersonShortDetail


class MovieRepository:
    """Repository for working with data from Netflix Movies service."""

    def __init__(self, movie_client: AsyncMovieClient) -> None:
        assert isinstance(movie_client, AsyncMovieClient)
        self._movie_client = movie_client

    async def find_movie_by_name(self, name: str, /) -> FilmShortDetail | None:
        """Find movie by name."""
        films = await self._movie_client.find_films(
            name, fetch_all=False, options=self._create_query_options(page_size=1))
        try:
            film = films[0]
        except (TypeError, IndexError):
            return None
        return FilmShortDetail(film_id=film.uuid, title=film.title, imdb_rating=film.imdb_rating)

    async def get_movie_by_id(self, film_id: uuid.UUID, /) -> FilmFullDetail:
        """Get film by id."""
        film = await self._movie_client.fetch_film_by_id(film_id)
        return FilmFullDetail(
            film_id=film_id,
            title=film.title,
            imdb_rating=film.imdb_rating,
            description=film.description,
            actors=", ".join([actors.full_name for actors in film.actors]),
            directors=", ".join([directors.full_name for directors in film.directors]),
        )

    async def find_person_by_name(self, person_name: str, /) -> PersonShortDetail | None:
        """Find person by name."""
        persons = await self._movie_client.find_persons(
            person_name, fetch_all=False, options=self._create_query_options(page_size=1))
        try:
            person = persons[0]
        except (TypeError, IndexError):
            return None
        return PersonShortDetail(
            person_id=person.uuid,
            full_name=person.full_name,
        )

    async def get_person_films(self, person_id: uuid.UUID, /) -> FilmList:
        """Get person's films."""
        films = await self._movie_client.fetch_person_films(person_id)
        return FilmList(films=", ".join([film.title for film in films]))

    @staticmethod
    def _create_query_options(*, page_size: int) -> QueryOptions:
        """Create query options for API request."""
        pagination_options = PageNumberPaginationOptions(page_size=page_size)
        return QueryOptions(page_number_pagination=pagination_options)
