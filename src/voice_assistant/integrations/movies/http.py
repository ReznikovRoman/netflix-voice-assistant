from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable, Iterable, Mapping

import requests

from . import exceptions
from .version import __version__

if TYPE_CHECKING:
    from .types import TimeoutTupleType, TimeoutType


def _exc_msg(exc: Exception) -> str:
    """Сообщение ошибки."""
    if (package := exc.__class__.__module__) == "__main__":
        package = __package__
    fullname = f"{package}.{exc.__class__.__qualname__}"
    if msg := str(exc):
        return f"{fullname}: {msg}"
    return fullname


class MoviesSession(requests.Session):
    """HTTP сессия для работы с API Netflix Movies."""

    base_api_path: str = "/api/v1"

    timeout: TimeoutTupleType = (30, 30)
    max_attempts: int = 3

    log = logging.getLogger(__name__)

    _base_request = requests.Session.request

    def __init__(
        self,
        base_url: str, *,
        timeout: TimeoutType | None = None,
        max_attempts: int | None = None,
    ) -> None:
        super().__init__()
        self.headers["User-Agent"] = f"movies.client/{__version__}"
        self.headers["Accept"] = "application/json,*/*;q=0.9"
        self.base_url = base_url.rstrip("/")
        self.base_api_url = f"{self.base_url}{self.base_api_path}"
        if timeout is not None:
            if isinstance(timeout, (int, float)):
                self.timeout = (timeout, timeout)
            else:
                self.timeout = tuple(timeout)
        if max_attempts is not None:
            assert max_attempts > 0
            self.max_attempts = max_attempts

    def request(self, method: str, url: str, *, max_attempts: int | None = None, **kwargs) -> requests.Response:
        log_msg = f"{method.upper()} {url}"
        if "params" in kwargs:
            log_msg = f"{log_msg} with query params: {kwargs['params']}"
        if "json" in kwargs:
            log_msg = f"{log_msg} with JSON body: {kwargs['json']}"
        self.log.debug(log_msg)
        if url.startswith("/"):
            url = f"{self.base_api_url}{url}"
        if max_attempts is None:
            max_attempts = self.max_attempts
        else:
            assert max_attempts > 0
        return self._retry(self._request, args=(method, url), kwargs=kwargs, max_attempts=max_attempts)

    def _request(self, method: str, url: str, *, timeout: TimeoutType | None = None, **kwargs) -> requests.Response:
        kwargs["timeout"] = timeout or self.timeout
        response = self._base_request(method, url, **kwargs)
        if response.ok:
            return response
        raise exceptions.HTTPError(response)

    def _retry(
        self, func: Callable[..., requests.Response], args: Iterable, kwargs: Mapping, max_attempts: int,
    ) -> requests.Response:
        _exc: Exception | None = None
        error_attempt = 1
        errors: list[Exception] = []
        while error_attempt <= max_attempts:
            try:
                return func(*args, **kwargs)
            except (OSError, exceptions.ServerError) as exc:
                self.log.warning(f"attempt {error_attempt} failed: {_exc_msg(exc)}")
                _exc = exc
                error_attempt += 1
                errors.append(exc)
        raise exceptions.MaxAttemptsError(errors, attempts=max_attempts) from _exc
