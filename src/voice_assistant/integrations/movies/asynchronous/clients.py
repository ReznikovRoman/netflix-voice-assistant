import logging
import uuid
from typing import AsyncIterator, ClassVar

from pydantic import parse_obj_as

from ..types import FilmDetail, FilmList, PersonFullDetail, PersonList, PersonShortDetail, QueryOptions
from ..warnings import InvalidPageSizeWarning
from .http import AsyncMoviesSession


class AsyncMovieClient:
    """Асинхронный клиент для работы с сервисом Netflix Movies."""

    MAX_PAGE_SIZE: ClassVar[int] = 999

    max_per_page: int = 100
    per_page: int = max_per_page

    log = logging.getLogger(__name__)

    _closed: bool = False

    def __init__(self, session: AsyncMoviesSession, *, per_page: int | None = None) -> None:
        self._session = session
        if per_page is not None:
            assert per_page > 0
            self.per_page = per_page

    @property
    def closed(self):
        return self._closed

    async def close(self) -> None:
        await self._session.close()
        self._closed = True

    async def get_paginated_response_iter(self, url: str, *, fetch_all: bool = True, **kwargs) -> AsyncIterator[dict]:
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
            async with self._session.get(url, **kwargs) as raw_response:
                response = await raw_response.json()
                assert isinstance(response, list)
                results_count = page * page_size
                if not response or (not fetch_all and results_count >= page_size):
                    break
                for result in response:
                    yield result
                page += 1

    async def get_film_by_id(self, film_id: uuid.UUID, /) -> FilmDetail:
        """Получение фильма по id."""
        async with self._session.get(f"/films/{film_id}") as raw_response:
            return FilmDetail.parse_obj(await raw_response.json())

    async def search_films_iter(
        self, query: str, /, *, fetch_all: bool = True, options: QueryOptions | None = None,
    ) -> AsyncIterator[FilmList]:
        """Поиск по фильмам. Возвращает итератор."""
        query_options = self._get_query_options(options).to_dict()
        query_options["query"] = query
        async for film in self.get_paginated_response_iter("/films/search", fetch_all=fetch_all, params=query_options):
            yield FilmList.parse_obj(film)

    async def search_films(
        self, query: str, /, *, fetch_all: bool = True, options: QueryOptions | None = None,
    ) -> list[FilmList]:
        """Поиск по фильмам."""
        query_options = self._get_query_options(options)
        return [film async for film in self.search_films_iter(query, fetch_all=fetch_all, options=query_options)]

    async def search_persons_iter(
        self, query: str, /, *, fetch_all: bool = True, options: QueryOptions | None = None,
    ) -> AsyncIterator[PersonList]:
        """Поиск по персонам."""
        query_options = self._get_query_options(options).to_dict()
        query_options["query"] = query
        results = self.get_paginated_response_iter("/persons/search", fetch_all=fetch_all, params=query_options)
        async for film in results:
            yield PersonList.parse_obj(film)

    async def search_persons(
        self, query: str, /, *, fetch_all: bool = True, options: QueryOptions | None = None,
    ) -> list[PersonList]:
        """Поиск по персонам."""
        query_options = self._get_query_options(options)
        return [person async for person in self.search_persons_iter(query, fetch_all=fetch_all, options=query_options)]

    async def get_person_short_details(self, person_id: uuid.UUID, /) -> PersonShortDetail:
        """Получение общей информации о персоне."""
        async with self._session.get(f"/persons/{person_id}") as raw_response:
            return PersonShortDetail.parse_obj(await raw_response.json())

    async def get_person_full_details(self, person_id: uuid.UUID, /) -> PersonFullDetail:
        """Получение полной информации о персоне."""
        async with self._session.get(f"/persons/full/{person_id}") as raw_response:
            return PersonFullDetail.parse_obj(await raw_response.json())

    async def get_person_films(self, person_id: uuid.UUID, /) -> list[FilmList]:
        """Получение списка фильмов персоны по id."""
        async with self._session.get(f"/persons/{person_id}/films") as raw_response:
            return parse_obj_as(list[FilmList], await raw_response.json())

    @staticmethod
    def _get_query_options(options: QueryOptions | None = None, /) -> QueryOptions:
        if options is None:
            return QueryOptions()
        return options


async def init_async_movie_client(session: AsyncMoviesSession) -> AsyncIterator[AsyncMovieClient]:
    """Инициализация асинхронного клиента Netflix Movies."""
    movie_client = AsyncMovieClient(session=session)
    yield movie_client
    await movie_client.close()
