import datetime
import uuid

from .clients import MovieClient
from .types import FilmDetail, FilmList, PersonFullDetail, PersonList, PersonShortDetail, QueryOptions
from .types.films import FilmAccessType, FilmAgeRating
from .types.roles import PersonRoleFilmList, Role

PERSON_ID = uuid.UUID("fb6a644b-436a-4131-8fbc-00ca73e9aee7")
PERSON_NAME = "Леонид Гайдай"

PERSON_SEARCH_RESULTS = [
    PersonList(uuid=PERSON_ID, full_name=PERSON_NAME),
]

FILM = FilmDetail(
    uuid=uuid.UUID("09445a09-bfb6-4eb1-84e8-c82b4fe80437"),
    title="Операция 'Ы'",
    imdb_rating=8.7,
    description=(
        "Студент Шурик попадает в самые невероятные ситуации: сражается с хулиганом Верзилой, "
        "весьма оригинальным способом готовится к экзамену и предотвращает «ограбление века», "
        "на которое идёт троица бандитов — Балбес, Трус и Бывалый."
    ),
    release_date=datetime.date(1965, 7, 23),
    age_rating=FilmAgeRating.GENERAL,
    access_type=FilmAccessType.PUBLIC,
    genre=[], actors=[], writers=[], directors=PERSON_SEARCH_RESULTS,
)

ANOTHER_FILM = FilmDetail(
    uuid=uuid.UUID("7e64ae94-4be9-4eaf-8f10-917e6ab2088c"),
    title="Кавказская пленница",
    imdb_rating=8.5,
    description=(
        "Отправившись в одну из горных республик собирать фольклор, "
        "студент Шурик влюбляется в симпатичную девушку Нину - спортсменку, отличницу, комсомолку и просто красавицу. "
        "Но её внезапно похищают банда их трёх человек, чтобы насильно выдать замуж. Наивный Шурик не сразу сообразил, "
        "что творится у него под носом, - однако затем отважно ринулся освобождать кавказскую пленницу."
    ),
    release_date=datetime.date(1967, 4, 1),
    age_rating=FilmAgeRating.GENERAL,
    access_type=FilmAccessType.PUBLIC,
    genre=[], actors=[], writers=[], directors=PERSON_SEARCH_RESULTS,
)

FILM_SEARCH_RESULTS = [
    FilmList(
        uuid=FILM.uuid,
        title=FILM.title,
        imdb_rating=FILM.imdb_rating,
        access_type=FILM.access_type,
    ),
    FilmList(
        uuid=ANOTHER_FILM.uuid,
        title=ANOTHER_FILM.title,
        imdb_rating=ANOTHER_FILM.imdb_rating,
        access_type=ANOTHER_FILM.access_type,
    ),
]

PERSON_SHORT_DETAILS = PersonShortDetail(
    uuid=PERSON_ID,
    full_name=PERSON_NAME,
    films_ids=[film.uuid for film in FILM_SEARCH_RESULTS],
)

PERSON_FULL_DETAILS = PersonFullDetail(
    uuid=PERSON_SHORT_DETAILS.uuid,
    full_name=PERSON_SHORT_DETAILS.full_name,
    roles=[
        PersonRoleFilmList(role=Role.DIRECTOR, films=FILM_SEARCH_RESULTS),
    ],
)


class MovieClientStub(MovieClient):
    """Стаб клиента для работы с сервисом Netflix Movies."""

    async def get_film_by_id(self, film_id: uuid.UUID, /) -> FilmDetail:
        return FILM

    async def search_films(self, query: str, /, *, options: QueryOptions | None = None) -> list[FilmList]:
        return FILM_SEARCH_RESULTS

    async def search_persons(self, query: str, /, *, options: QueryOptions | None = None) -> list[PersonList]:
        return PERSON_SEARCH_RESULTS

    async def get_person_short_details(self, person_id: uuid.UUID, /) -> PersonShortDetail:
        return PERSON_SHORT_DETAILS

    async def get_person_full_details(self, person_id: uuid.UUID, /) -> PersonFullDetail:
        return PERSON_FULL_DETAILS

    async def get_person_films(self, person_id: uuid.UUID, /) -> list[FilmList]:
        return FILM_SEARCH_RESULTS
