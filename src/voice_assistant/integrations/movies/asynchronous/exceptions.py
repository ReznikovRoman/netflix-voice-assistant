from __future__ import annotations

import logging
from http import HTTPStatus
from typing import ClassVar, Iterable, Type

import aiohttp

from ..exceptions import NetflixMoviesBaseError

log = logging.getLogger(__name__)


class AsyncNetflixMoviesError(NetflixMoviesBaseError):
    """Ошибка от сервиса Netflix Movies."""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self}>"


class AsyncMaxAttemptsError(AsyncNetflixMoviesError):
    """Превышен лимит повторных запросов к АПИ."""

    errors: tuple[Exception]
    attempts: int

    def __init__(self, errors: Iterable[Exception], *, attempts: int) -> None:
        self.errors = tuple(errors)
        self.attempts = attempts

    def __str__(self) -> str:
        return ", ".join(f"<{error.__class__.__name__}: {error}>" for error in self.errors)

    @property
    def last_error(self):
        return self.errors[-1]


class _AsyncHTTPError(AsyncNetflixMoviesError):

    _code: str
    _message: str
    _error_dict: dict | None

    def __init__(
        self, response: aiohttp.ClientResponse, error_code: HTTPStatus, error_dict: dict | None = None,
    ) -> None:
        self.response = response
        self.error_code = error_code
        self.error_dict = error_dict

    @property
    def status_code(self) -> HTTPStatus:
        return HTTPStatus(self.response.status)

    @property
    def code(self) -> str:
        _code = None
        if self.error_dict:
            _code = self.error_dict.get("error", {}).get("code")
        elif self.response.text:
            _code = self.response.text
        self._message = _code or "_server_error"
        return self._message

    @property
    def message(self) -> str:
        _message = None
        if self.error_dict:
            _message = self.error_dict.get("error", {}).get("message")
        elif self.response.text:
            _message = self.response.text
        self._message = _message or None
        return self._message

    def __str__(self) -> str:
        return f"{self.status_code}: {self.message}"


class AsyncHTTPError(_AsyncHTTPError):
    """HTTP ошибка сервиса Netflix Movies."""

    _error_code_subclass_map: ClassVar[dict[str: Type["AsyncHTTPError"]]] = {}

    def __new__(
        cls, response: aiohttp.ClientResponse, error_code: HTTPStatus, error_dict: dict | None = None,
    ) -> AsyncHTTPError:
        if cls is not AsyncHTTPError:
            # Явно используется подкласс HTTPAsyncError -> не используем кастомный конструктор с диспатчером.
            return _AsyncHTTPError.__new__(cls, response, error_code, error_dict)
        status_code = response.status
        actual_class = cls._error_code_subclass_map.get(cls._get_error_code_from_response(error_dict))
        if not actual_class:
            if 400 <= status_code <= 499:
                actual_class = AsyncClientError
            elif 500 <= status_code <= 599:
                actual_class = AsyncServerError
            else:
                actual_class = AsyncHTTPError
        if "__new__" in actual_class.__dict__:
            return actual_class(response, error_code, error_dict)
        return _AsyncHTTPError.__new__(actual_class, response, error_code, error_dict)

    def __init__(
        self, response: aiohttp.ClientResponse, error_code: HTTPStatus, error_dict: dict | None = None,
    ) -> None:
        self.response = response
        self.error_code = error_code
        self.error_dict = error_dict

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if "code" in cls.__dict__:
            cls._error_code_subclass_map[cls.code] = cls

    def to_dict(self) -> dict:
        dct = {
            "error": {
                "code": self.code,
                "message": self.message,
            },
        }
        return dct

    @staticmethod
    def _get_error_code_from_response(response: dict, /) -> str:
        return response.get("error").get("code")


class AsyncServerError(AsyncHTTPError):
    """Ошибка сервера Netflix Movies."""


class AsyncClientError(AsyncHTTPError):
    """Ошибка при запросе."""


class AsyncNotFoundError(AsyncClientError):
    """Ресурс не найден."""

    code = "not_found"


class AsyncAuthorizationError(AsyncClientError):
    """Ошибка при авторизации."""

    code = "authorization_error"
