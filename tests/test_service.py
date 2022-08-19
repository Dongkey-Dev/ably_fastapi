import pytest

api_service_users = "/api/service/users"


@pytest.mark.asyncio
async def test_get_users(async_app_client, session):
    response = await async_app_client.get(url=api_service_users)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_one(async_app_client, session, user_1):
    session.add(user_1)
    await session.commit()
    response = await async_app_client.get(url=api_service_users)
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_user_two(async_app_client, session, user_1, user_2):
    session.add(user_1)
    session.add(user_2)
    await session.commit()
    response = await async_app_client.get(url=api_service_users)
    assert len(response.json()) == 2
