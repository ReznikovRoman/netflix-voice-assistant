import uuid

from .types import FilmDetail, FilmList, PersonFullDetail, PersonList, PersonShortDetail, QueryOptions


class MovieClient:
    """Клиент для работы с сервисом Netflix Movies."""

    async def get_film_by_id(self, film_id: uuid.UUID, /) -> FilmDetail:
        """Получение фильма по id."""

    async def search_films(self, query: str, /, *, options: QueryOptions | None = None) -> list[FilmList]:
        """Поиск по фильмам."""
        query_options = self._get_query_options(options)  # noqa: F841  # TODO: remove `noqa`

    async def search_persons(self, query: str, /, *, options: QueryOptions | None = None) -> list[PersonList]:
        """Поиск по персонам."""
        query_options = self._get_query_options(options)  # noqa: F841  # TODO: remove `noqa`

    async def get_person_short_details(self, person_id: uuid.UUID, /) -> PersonShortDetail:
        """Получение общей информации о персоне."""

    async def get_person_full_details(self, person_id: uuid.UUID, /) -> PersonFullDetail:
        """Получение полной информации о персоне."""

    async def get_person_films(self, person_id: uuid.UUID, /) -> list[FilmList]:
        """Получение списка фильмов персоны по id."""

    @staticmethod
    def _get_query_options(options: QueryOptions | None = None, /) -> QueryOptions:
        if options is None:
            return QueryOptions()
        return options
