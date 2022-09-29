import logging
import uuid
from typing import ClassVar, Iterator

from pydantic import parse_obj_as

from .http import MoviesSession
from .types import FilmDetail, FilmList, PersonFullDetail, PersonList, PersonShortDetail, QueryOptions
from .warnings import InvalidPageSizeWarning


class MovieClient:
    """Клиент для работы с сервисом Netflix Movies."""

    MAX_PAGE_SIZE: ClassVar[int] = 999

    max_per_page: int = 100
    per_page: int = max_per_page

    log = logging.getLogger(__name__)

    _closed: bool = False

    def __init__(self, session: MoviesSession, *, per_page: int | None = None) -> None:
        self._session = session
        if per_page is not None:
            assert per_page > 0
            self.per_page = per_page

    @property
    def closed(self):
        return self._closed

    def close(self) -> None:
        """Закрытие HTTP сессии."""
        self._session.close()
        self._closed = True

    def get_paginated_response_iter(self, url: str, *, fetch_all: bool = True, **kwargs) -> Iterator[dict]:
        """Получение итератора по пагинированному ответу."""
        page = 0
        params = kwargs.setdefault("params", {})
        page_size = kwargs["params"].get("page[size]") or self.per_page
        params["page[size]"] = page_size
        if not fetch_all and page_size > self.MAX_PAGE_SIZE:
            page_size = self.MAX_PAGE_SIZE
            InvalidPageSizeWarning.warn(
                f"Invalid query param: `page[size]` must be in range [1, {self.MAX_PAGE_SIZE}].")
        while True:
            params["page[number]"] = page
            response = self._session.get(url, **kwargs).json()
            assert isinstance(response, list)
            results_count = page * page_size
            if not response or (not fetch_all and results_count >= page_size):
                break
            yield from response
            page += 1

    def get_film_by_id(self, film_id: uuid.UUID, /) -> FilmDetail:
        """Получение фильма по id."""
        return FilmDetail.parse_obj(self._session.get(f"/films/{film_id}").json())

    def search_films_iter(
        self, query: str, /, *, fetch_all: bool = True, options: QueryOptions | None = None,
    ) -> Iterator[FilmList]:
        """Поиск по фильмам. Возвращает итератор."""
        query_options = self._get_query_options(options).to_dict()
        query_options["query"] = query
        for film in self.get_paginated_response_iter("/films/search", fetch_all=fetch_all, params=query_options):
            yield FilmList.parse_obj(film)

    def search_films(
        self, query: str, /, *, fetch_all: bool = True, options: QueryOptions | None = None,
    ) -> list[FilmList]:
        """Поиск по фильмам."""
        query_options = self._get_query_options(options)
        return list(self.search_films_iter(query, fetch_all=fetch_all, options=query_options))

    def search_persons_iter(
        self, query: str, /, *, fetch_all: bool = True, options: QueryOptions | None = None,
    ) -> Iterator[PersonList]:
        """Поиск по персонам."""
        query_options = self._get_query_options(options).to_dict()
        query_options["query"] = query
        for person in self.get_paginated_response_iter("/persons/search", fetch_all=fetch_all, params=query_options):
            yield PersonList.parse_obj(person)

    def search_persons(
        self, query: str, /, *, fetch_all: bool = True, options: QueryOptions | None = None,
    ) -> list[PersonList]:
        """Поиск по персонам."""
        query_options = self._get_query_options(options)
        return list(self.search_persons_iter(query, fetch_all=fetch_all, options=query_options))

    def get_person_short_details(self, person_id: uuid.UUID, /) -> PersonShortDetail:
        """Получение общей информации о персоне."""
        return PersonShortDetail.parse_obj(self._session.get(f"/persons/{person_id}").json())

    def get_person_full_details(self, person_id: uuid.UUID, /) -> PersonFullDetail:
        """Получение полной информации о персоне."""
        return PersonFullDetail.parse_obj(self._session.get(f"/persons/full/{person_id}").json())

    def get_person_films(self, person_id: uuid.UUID, /) -> list[FilmList]:
        """Получение списка фильмов персоны по id."""
        return parse_obj_as(list[FilmList], self._session.get(f"/persons/{person_id}/films").json())

    @staticmethod
    def _get_query_options(options: QueryOptions | None = None, /) -> QueryOptions:
        if options is None:
            return QueryOptions()
        return options


def init_movie_client(session: MoviesSession) -> Iterator[MovieClient]:
    """Инициализация клиента Netflix Movies."""
    movie_client = MovieClient(session=session)
    yield movie_client
    movie_client.close()
