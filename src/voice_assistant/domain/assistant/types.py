from pydantic import BaseModel


class AssistantRequest(BaseModel):
    """Базовый класс запроса."""

    pass


class AssistantResponse(BaseModel):
    """Базовый класс ответа."""

    pass
