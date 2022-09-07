from fastapi import APIRouter

from .handlers import misc

api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(misc.router)
