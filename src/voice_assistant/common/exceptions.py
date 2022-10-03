from http import HTTPStatus


class APIErrorMixin:
    """REST API error mixin."""

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
    """Base service error."""


class NetflixVoiceAssistantError(APIErrorMixin, BaseNetflixVoiceAssistantError):
    """Netflix Voice Assistant service error."""


class NotFoundError(NetflixVoiceAssistantError):
    """Resource is not found."""

    message = "Resource not found"
    code = "not_found"
    status_code = HTTPStatus.NOT_FOUND


class ConflictError(NetflixVoiceAssistantError):
    """Resource conflict."""

    message = "Resource cannot be processed"
    code = "resource_conflict"
    status_code = HTTPStatus.CONFLICT


class ImproperlyConfiguredError(NetflixVoiceAssistantError):
    """Improperly configured service."""

    message = "Improperly configured service"
    code = "improperly_configured"
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR


class AuthorizationError(NetflixVoiceAssistantError):
    """Authorization error."""

    message = "Authorization error"
    code = "authorization_error"
    status_code = HTTPStatus.UNAUTHORIZED


class RequiredHeaderMissingError(NetflixVoiceAssistantError):
    """Required header is missing in the request."""

    message = "Required header is missing"
    code = "missing_header"
    status_code = HTTPStatus.BAD_REQUEST
