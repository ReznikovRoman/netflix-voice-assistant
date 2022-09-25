from http import HTTPStatus

from voice_assistant.common.exceptions import BaseNetflixVoiceAssistantError, NetflixVoiceAssistantError


class UnknownAssistantProvider(NetflixVoiceAssistantError):
    """Неизвестный провайдер голосового ассистента."""

    message = "Unknown assistant provider"
    code = "unknown_assistant_provider"
    status_code = HTTPStatus.BAD_REQUEST


class FilmNotFoundError(BaseNetflixVoiceAssistantError):
    """Фильм по данному названию не найден."""
