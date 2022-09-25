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
        films = await self._movie_client.search_films(name, options=self._create_query_options(page_size=1))
        try:
            film = films[0]
        except TypeError:
            return None
        return FilmShortDetail(film_id=film.uuid, title=film.title, imdb_rating=film.imdb_rating)

    async def get_movie_by_id(self, film_id: uuid.UUID, /) -> FilmFullDetail:
        """Получение фильма по id."""
        film = await self._movie_client.get_film_by_id(film_id)
        return FilmFullDetail(
            film_id=film_id,
            title=film.title,
            imdb_rating=film.imdb_rating,
            description=film.description,
            actors=" ".join([actors.full_name for actors in film.actors]),
            directors=" ".join([directors.full_name for directors in film.directors]),
        )

    async def find_person_by_name(self, person_name: str, /) -> PersonShortDetail | None:
        """Поиск по персоне."""
        persons = await self._movie_client.search_persons(person_name, options=self._create_query_options(page_size=1))
        try:
            person = persons[0]
        except TypeError:
            return None
        return PersonShortDetail(
            person_id=person.uuid,
            full_name=person.full_name,
        )

    async def get_person_films(self, person_id: uuid.UUID, /) -> FilmList:
        """Получение фильмов с участием данной персоны."""
        films = await self._movie_client.get_person_films(person_id)
        return FilmList(films=", ".join([film.title for film in films]))

    @staticmethod
    def _create_query_options(*, page_size: int) -> QueryOptions:
        """Создание настроек для запроса."""
        pagination_options = PageNumberPaginationOptions(page_size=page_size)
        return QueryOptions(page_number_pagination=pagination_options)
