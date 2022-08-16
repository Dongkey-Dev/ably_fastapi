import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_users(async_app_client):
    response = await async_app_client.get("/api/service/users")
    assert response.status_code == 200
