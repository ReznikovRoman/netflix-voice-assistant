from http import HTTPStatus

from dependency_injector.wiring import Provide, inject

from fastapi import APIRouter, Body, Depends, Path

from voice_assistant.containers import Container
from voice_assistant.domain.assistant import AssistantProviderDispatcher
from voice_assistant.domain.assistant.enums import AssistantProviderSlug

router = APIRouter(tags=["Assistant"])


@router.post("/requests/process/{provider}", summary="Webhook for provider", status_code=HTTPStatus.OK)
@inject
async def process_user_request(
    provider: AssistantProviderSlug = Path(..., title="Provider slug."),
    payload: dict = Body(..., description="Provider data"), *,
    provider_dispatcher: AssistantProviderDispatcher = Depends(Provide[Container.assistant_dispatcher]),
):
    """Handle request from provider."""
    return await provider_dispatcher.dispatch_provider(provider, data=payload)
