import pytest


@pytest.mark.asyncio
async def test_get_users(async_app_client, session):
    response = await async_app_client.get("/api/service/users")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_one(logger, async_app_client, session, user_1):
    session.add(user_1)
    await session.commit()
    response = await async_app_client.get(url="/api/service/users")
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_user_two(async_app_client, session, user_1, user_2):
    session.add(user_1)
    session.add(user_2)
    await session.commit()
    response = await async_app_client.get(url="/api/service/users")
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_verify_phone_to_regist_user(logger, async_app_client, session, post_body_verify_phone_to_regist_user):
    response = await async_app_client.post(url="/api/auth/verify_phone_to_regist", json=post_body_verify_phone_to_regist_user)
    logger.info(response.json())
    k, v = response.json().popitem()
    assert "Authorization" in k
    assert "Bearer" in v
