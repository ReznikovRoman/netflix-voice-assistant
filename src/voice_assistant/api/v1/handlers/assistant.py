from http import HTTPStatus

from dependency_injector.wiring import Provide, inject

from fastapi import APIRouter, Depends, Request

from voice_assistant.containers import Container
from voice_assistant.domain.assistant import AssistantProviderDispatcher
from voice_assistant.domain.assistant.enums import AssistantProviderSlug

router = APIRouter(
    tags=["Assistant"],
)


@router.post("/requests/process", summary="Webhook для ассистента", status_code=HTTPStatus.OK)
@inject
async def process_user_request(
    request: Request,
    provider: AssistantProviderSlug, *,
    provider_dispatcher: AssistantProviderDispatcher = Depends(Provide[Container.assistant_dispatcher]),
):
    """Обработка запроса от пользователя."""
    return await provider_dispatcher.dispatch_provider(provider, request=request)
