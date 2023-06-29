from fastapi import APIRouter

router = APIRouter(tags=["Misc"])


@router.get("/healthcheck", summary="Service health")
async def healthcheck():
    """Check service health."""
    return {"status": "ok 2"}
