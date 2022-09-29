from __future__ import annotations

import logging
from functools import cached_property
from http import HTTPStatus
from typing import ClassVar, Iterable, Type

import requests

log = logging.getLogger(__name__)


class NetflixMoviesBaseError(Exception):
    """Базовая ошибка от сервиса Netflix Movies."""


class NetflixMoviesError(NetflixMoviesBaseError):
    """Ошибка от сервиса Netflix Movies."""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self}>"


class MaxAttemptsError(NetflixMoviesError):
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


class _HTTPError(NetflixMoviesError):

    _code: str
    _message: str
    _error_dict: dict | None

    def __init__(self, response: requests.Response) -> None:
        self.response = response

    @property
    def status_code(self) -> HTTPStatus:
        return HTTPStatus(self.response.status_code)

    @cached_property
    def error_dict(self) -> dict | None:
        try:
            response_json = self.response.json()
        except ValueError:
            self._error_dict = None
            return None
        if not isinstance(response_json, dict):
            log.warning(f"Unexpected error body: {response_json!r}")
            self._error_dict = None
        else:
            self._error_dict = response_json
        return self._error_dict

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


class HTTPError(_HTTPError):
    """HTTP ошибка сервиса Netflix Movies."""

    _error_code_subclass_map: ClassVar[dict[str: Type["HTTPError"]]] = {}

    def __new__(cls, response: requests.Response) -> HTTPError:
        if cls is not HTTPError:
            # Явно используется подкласс HTTPError -> не используем кастомный конструктор с диспатчером.
            return _HTTPError.__new__(cls, response)
        status_code = response.status_code
        actual_class = cls._error_code_subclass_map.get(cls._get_error_code_from_response(response))
        if not actual_class:
            if 400 <= status_code <= 499:
                actual_class = ClientError
            elif 500 <= status_code <= 599:
                actual_class = ServerError
            else:
                actual_class = HTTPError
        if "__new__" in actual_class.__dict__:
            return actual_class(response)
        return _HTTPError.__new__(actual_class, response)

    def __init__(self, response: requests.Response) -> None:
        self.response = response

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
    def _get_error_code_from_response(response: requests.Response, /) -> str:
        return response.json().get("error").get("code")


class ServerError(HTTPError):
    """Ошибка сервера Netflix Movies."""


class ClientError(HTTPError):
    """Ошибка при запросе."""


class NotFoundError(ClientError):
    """Ресурс не найден."""

    code = "not_found"


class AuthorizationError(ClientError):
    """Ошибка при авторизации."""

    code = "authorization_error"
