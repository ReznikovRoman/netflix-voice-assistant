from http import HTTPStatus

from .types.common import BaseOrjsonSchema


class NetflixMoviesHTTPErrorIn(BaseOrjsonSchema):
    """Ошибка, полученная от АПИ сервиса Netflix Movies."""

    message: str
    code: str
    status_code: HTTPStatus


class APIErrorMixin:
    """Миксин для ошибки REST API."""

    message: str
    code: str
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message: str | None = None, code: str | None = None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __str__(self) -> str:
        return self.message

    def to_dict(self) -> dict:
        dct = {
            "error": {
                "code": self.code,
                "message": self.message,
            },
        }
        return dct


class NetflixMoviesError(Exception):
    """Ошибка от сервиса Netflix Movies."""


class NetflixMoviesHTTPError(APIErrorMixin, NetflixMoviesError):
    """HTTP ошибка сервиса Netflix Movies."""


class NotFoundError(NetflixMoviesHTTPError):
    """Ресурс не найден."""

    message = "Resource not found"
    code = "not_found"
    status_code = HTTPStatus.NOT_FOUND


class AuthorizationError(NetflixMoviesHTTPError):
    """Ошибка при авторизации."""

    message = "Authorization error"
    code = "authorization_error"
    status_code = HTTPStatus.UNAUTHORIZED
