from http import HTTPStatus

from fastapi import APIRouter, Request

from voice_assistant.domain.assistant import AssistantProviderDispatcher
from voice_assistant.domain.assistant.enums import AssistantProviderSlug

router = APIRouter(
    tags=["Assistant"],
)


@router.post("/requests/process", summary="Webhook для ассистента", status_code=HTTPStatus.OK)
async def process_user_request(
    request: Request,
    provider: AssistantProviderSlug, *,
    provider_dispatcher: AssistantProviderDispatcher,
):
    """Обработка запроса от пользователя."""
    # XXX: Пример вебхука для Алисы: .../process?provider=yandex_alice
    # TODO: брать только необходимые данные из request
    # TODO: в response_model будет несколько возможных вариантов ответа
    #  - FastAPI anyOf docs: https://fastapi.tiangolo.com/tutorial/extra-models/#union-or-anyof
    return provider_dispatcher.dispatch_provider(provider)