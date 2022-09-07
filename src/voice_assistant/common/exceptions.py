from http import HTTPStatus


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


class BaseNetflixVoiceAssistantError(Exception):
    """Базовая ошибка сервиса."""


class NetflixVoiceAssistantError(APIErrorMixin, BaseNetflixVoiceAssistantError):
    """Ошибка сервиса Netflix Voice Assistant."""


class NotFoundError(NetflixVoiceAssistantError):
    """Ресурс не найден."""

    message = "Resource not found"
    code = "not_found"
    status_code: int = HTTPStatus.NOT_FOUND


class ConflictError(NetflixVoiceAssistantError):
    """Конфликт между существующими ресурсами."""

    message = "Resource cannot be processed"
    code = "resource_conflict"
    status_code: int = HTTPStatus.CONFLICT


class ImproperlyConfiguredError(NetflixVoiceAssistantError):
    """Неверная конфигурация."""

    message = "Improperly configured service"
    code = "improperly_configured"
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR


class AuthorizationError(NetflixVoiceAssistantError):
    """Ошибка при авторизации."""

    message = "Authorization error"
    code = "authorization_error"
    status_code = HTTPStatus.UNAUTHORIZED


class RequiredHeaderMissingError(NetflixVoiceAssistantError):
    """Отсутствует обязательный заголовок в запросе."""

    message = "Required header is missing"
    code = "missing_header"
    status_code: int = HTTPStatus.BAD_REQUEST
