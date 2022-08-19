import time

import pytest
from app.common.consts import JWT_REGIST_DELTA_TIME_MINUTE
from app.jwt.jwt_handler import jwt_decode

sec = 1
minute = sec * 60
api_auth_verify_phone_to_regist = "/api/auth/verify_phone_to_regist"
api_auth_regist_user = "/api/auth/user"


@pytest.mark.asyncio
async def test_verify_phone_to_regist_user(logger, async_app_client, session, post_body_verify_phone_to_regist_user_1):
    response = await async_app_client.post(url=api_auth_verify_phone_to_regist, json=post_body_verify_phone_to_regist_user_1)
    logger.info(response.json())
    k, v = response.json().popitem()
    assert "Authorization" in k
    assert "Bearer" in v
    time.time().__int__()
    payload = await jwt_decode(v)
    assert payload.get(
        "phone") == post_body_verify_phone_to_regist_user_1.get("phone")
    assert payload.get("exp") == time.time().__int__() + \
        JWT_REGIST_DELTA_TIME_MINUTE*minute


@pytest.mark.asyncio
async def test_regist_user(logger, async_app_client, session, post_body_verify_phone_to_regist_user_1, post_body_regist_user_1):
    response_jwt = await async_app_client.post(url=api_auth_verify_phone_to_regist, json=post_body_verify_phone_to_regist_user_1)
    response = await async_app_client.post(url=api_auth_regist_user, headers=response_jwt.json(), json=post_body_regist_user_1)
    assert response.status_code == 201
