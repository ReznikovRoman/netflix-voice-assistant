import pytest

pytestmark = [pytest.mark.asyncio]


async def test_ok(client):
    """Эндпоинт /healthcheck отдает 200 статус."""
    response = await client.get("/api/v1/healthcheck")

    assert response["status"] == "ok"
