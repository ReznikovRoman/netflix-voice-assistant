from fastapi import APIRouter

from .handlers import assistant, misc

api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(assistant.router, prefix="/assistants")

# Miscellaneous
api_v1_router.include_router(misc.router)
