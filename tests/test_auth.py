import time

import bcrypt
import pytest
import sqlalchemy as sa
from app.common.consts import (JWT_LOGIN_DELTA_TIME_MINUTE,
                               JWT_REGIST_DELTA_TIME_MINUTE)
from app.jwt.jwt_handler import jwt_decode
from app.utils import query_utils as qu

sec = 1
minute = sec * 60
api_auth_verify_phone_to_regist = "/api/auth/verify_phone_to_regist"
api_auth_verify_phone_to_reset_pswd = "/api/auth/verify_phone_to_reset_pswd"
api_auth_user = "/api/auth/user"
api_auth_login = "/api/auth/login"


@pytest.mark.asyncio
async def test_verify_phone_to_regist_user_1(
        async_app_client,
        post_body_verify_phone_to_regist_user_1):
    response = await async_app_client.post(url=api_auth_verify_phone_to_regist, json=post_body_verify_phone_to_regist_user_1)
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
async def test_regist_user_1(
        async_app_client,
        post_body_verify_phone_to_regist_user_1,
        post_body_regist_user_1):
    response_jwt = await async_app_client.post(url=api_auth_verify_phone_to_regist, json=post_body_verify_phone_to_regist_user_1)
    response = await async_app_client.post(url=api_auth_user, headers=response_jwt.json(), json=post_body_regist_user_1)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_verify_phone_to_reset_user_1(
        session, async_app_client,
        post_body_verify_phone_to_regist_user_1,
        post_body_regist_user_1, user_class):
    response_jwt = await async_app_client.post(url=api_auth_verify_phone_to_regist, json=post_body_verify_phone_to_regist_user_1)
    await async_app_client.post(url=api_auth_user, headers=response_jwt.json(), json=post_body_regist_user_1)
    response = await async_app_client.post(url=api_auth_verify_phone_to_reset_pswd, json=post_body_verify_phone_to_regist_user_1)
    k, v = response.json().popitem()
    assert "Authorization" in k
    assert "Bearer" in v
    time.time().__int__()
    payload = await jwt_decode(v)

    inserted_user = await session.execute(sa.select(user_class))
    inserted_user = inserted_user.scalar_one_or_none()
    assert inserted_user
    assert payload.get(
        "phone") == post_body_verify_phone_to_regist_user_1.get("phone")
    assert payload.get("exp") == time.time().__int__() + \
        JWT_REGIST_DELTA_TIME_MINUTE*minute
    assert payload.get("doublehash_pswd") == await qu.get_hash_pswd(
        inserted_user.pswd)


@pytest.mark.asyncio
async def test_login_user_1(
        user_1, async_app_client,
        post_body_verify_phone_to_regist_user_1,
        post_body_regist_user_1,
        post_body_login_user_1):
    response_jwt = await async_app_client.post(url=api_auth_verify_phone_to_regist, json=post_body_verify_phone_to_regist_user_1)
    await async_app_client.post(url=api_auth_user, headers=response_jwt.json(), json=post_body_regist_user_1)
    response = await async_app_client.post(url=api_auth_login, json=post_body_login_user_1)
    _, v = response.json().popitem()
    payload = await jwt_decode(v)
    assert payload.get('email') == user_1.email
    assert payload.get("exp") == time.time().__int__() + \
        JWT_LOGIN_DELTA_TIME_MINUTE*minute


@pytest.mark.asyncio
async def test_reset_pswd_user_1(
        session, user_1, async_app_client,
        post_body_verify_phone_to_regist_user_1,
        post_body_regist_user_1,
        post_body_reset_pswd_user_1, user_class):
    response_jwt = await async_app_client.post(url=api_auth_verify_phone_to_regist, json=post_body_verify_phone_to_regist_user_1)
    await async_app_client.post(url=api_auth_user, headers=response_jwt.json(), json=post_body_regist_user_1)
    response_jwt = await async_app_client.post(url=api_auth_verify_phone_to_reset_pswd, json=post_body_verify_phone_to_regist_user_1)
    await async_app_client.put(url=api_auth_user, json=post_body_reset_pswd_user_1, headers=response_jwt.json())

    reseted_user = await session.execute(sa.select(user_class))
    reseted_user = reseted_user.scalar_one_or_none()
    is_verified = bcrypt.checkpw(post_body_reset_pswd_user_1.get("pswd").encode("utf-8"),
                                 reseted_user.pswd.encode("utf-8"))
    assert is_verified
