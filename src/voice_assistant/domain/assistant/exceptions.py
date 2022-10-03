from http import HTTPStatus

from voice_assistant.common.exceptions import BaseNetflixVoiceAssistantError, NetflixVoiceAssistantError


class UnknownAssistantProvider(NetflixVoiceAssistantError):
    """Unknown voice assistant provider."""

    message = "Unknown assistant provider"
    code = "unknown_assistant_provider"
    status_code = HTTPStatus.BAD_REQUEST


class FilmNotFoundError(BaseNetflixVoiceAssistantError):
    """Film was not found by the given query."""
