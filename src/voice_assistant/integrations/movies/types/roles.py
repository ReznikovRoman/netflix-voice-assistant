from enum import Enum

from .common import BaseIdOrjsonSchema, BaseOrjsonSchema
from .films import FilmList


class Role(str, Enum):
    """Роль персоны."""

    ACTOR = "actor"
    WRITER = "writer"
    DIRECTOR = "director"


class PersonRoleFilmList(BaseOrjsonSchema):
    """Роль персоны со списком фильмов."""

    role: Role
    films: list[FilmList]


class PersonFullDetail(BaseIdOrjsonSchema):
    """Персона (с разбиением фильмов по ролям)."""

    full_name: str
    roles: list[PersonRoleFilmList]