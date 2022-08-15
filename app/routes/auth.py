import hashlib

import bcrypt
from app.common.consts import (JWT_LOGIN_DELTA_TIME_MINUTE,
                               JWT_REGIST_DELTA_TIME_MINUTE)
from app.db.dbconn import get_db_session
from app.db.schema import Users
from app.middleware.jwt_handler import (create_access_token,
                                        get_phone_hashpswd_token,
                                        get_phone_token)
from app.models import (MessageOut, ResetPswdIn, Token, UserLoginIn,
                        UserPhonePswdToken, UserPhoneToken, UserRegistIn,
                        UserToken, ValidPhoneIn)
from app.utils.open_api_docs import auth_scheme
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

router = APIRouter()


@router.post("/auth/verify_phone_to_regist", status_code=202, response_model=Token)
async def verify_phone_to_regist(phone_info: ValidPhoneIn, session: AsyncSession = Depends(get_db_session)):
    is_exist = await is_phone_exist(session, phone_info.phone)
    if not (phone_info.phone and phone_info.username):
        return JSONResponse(status_code=400, content=dict(msg="Some infomation is missing."))
    if is_exist:
        return JSONResponse(status_code=400, content=dict(msg="Already registered phone number."))
    data = UserPhoneToken.from_orm(phone_info).dict()
    token = dict(
        Authorization=f"Bearer {create_access_token(data=data, expires_delta=JWT_REGIST_DELTA_TIME_MINUTE)}"
    )
    return token


@router.post("/auth/user", status_code=201, response_model=MessageOut, dependencies=[Depends(auth_scheme)])
async def regist_user(reg_info: UserRegistIn, session: AsyncSession = Depends(get_db_session), token_data: UserPhoneToken = Depends(get_phone_token)):
    is_exist = await is_email_exist(session, reg_info.email)
    if not (reg_info.email and reg_info.pswd and
            reg_info.nickname and reg_info.username and
            reg_info.phone and reg_info.confirm_pswd):
        return JSONResponse(status_code=400, content=dict(msg="Some infomation is missing."))
    if reg_info.phone != token_data.phone:
        return JSONResponse(status_code=400, content=dict(msg="The wrong phone number."))
    if is_exist:
        return JSONResponse(status_code=400, content=dict(msg="Email already exists."))
    hashed_pswd = bcrypt.hashpw(
        reg_info.pswd.encode("utf-8"), bcrypt.gensalt())
    inserted_user = await create_user(session, email=reg_info.email, pswd=hashed_pswd.decode(),
                                      nickname=reg_info.nickname, phone=reg_info.phone, username=reg_info.username)
    return MessageOut(msg=f"{reg_info.email} regist success.")


@router.post("/auth/verify_phone_to_reset_pswd", status_code=202, response_model=Token)
async def verify_phone_to_reset_pswd(phone_info: ValidPhoneIn):
    user_to_reset = await is_phone_exist(phone_info.phone)
    if not (phone_info.phone and phone_info.username):
        return JSONResponse(status_code=400, content=dict(msg="Some infomation is missing."))
    if not user_to_reset:
        return JSONResponse(status_code=400, content=dict(msg="There is no match user"))
    user_pswd = user_to_reset.pswd
    doublehash_pswd = await get_hash_pswd(user_pswd)
    token_data = UserPhonePswdToken(
        phone=phone_info.phone, doublehash_pswd=doublehash_pswd)
    token = dict(
        Authorization=f"Bearer {create_access_token(data=UserPhonePswdToken.from_orm(token_data).dict(), expires_delta=JWT_REGIST_DELTA_TIME_MINUTE)}"
    )
    return token


@router.patch("/auth/user_pswd", status_code=201, response_model=MessageOut, dependencies=[Depends(auth_scheme)])
async def reset_pswd(reset_info: ResetPswdIn, phone_pswd_token: UserPhonePswdToken = Depends(get_phone_hashpswd_token)):
    user_to_reset_pswd = await is_email_exist(reset_info.email)
    doublehash_pswd = await get_hash_pswd(user_to_reset_pswd.pswd)
    if not (reset_info.email and reset_info.pswd and reset_info.confirm_pswd):
        return JSONResponse(status_code=400, content=dict(msg="Some infomation is missing."))
    if not user_to_reset_pswd:
        return JSONResponse(status_code=400, content=dict(msg="There is no match user."))
    if phone_pswd_token.doublehash_pswd != doublehash_pswd:
        return JSONResponse(status_code=400, content=dict(msg=f"Looks like already reset password or wrong email. \n {phone_pswd_token} {doublehash_pswd}"))
    hashed_pswd = bcrypt.hashpw(
        reset_info.pswd.encode("utf-8"), bcrypt.gensalt())
    ret = Users.filter(email=reset_info.email).update(
        auto_commit=True, pswd=hashed_pswd.decode())
    return MessageOut(msg=f"{user_to_reset_pswd.email} password updated. {ret}")


@router.post("/auth/login_user", status_code=202, response_model=Token)
async def login_to_get_token_which_can_call_api_me(log_info: UserLoginIn):
    is_exist = await is_email_exist(log_info.email)
    if not (log_info.email and log_info.pswd):
        return JSONResponse(status_code=400, content=dict(msg="Email and PW must be provided'"))
    if not is_exist:
        return JSONResponse(status_code=400, content=dict(msg="There is no match user"))
    user_to_log = Users.get(email=log_info.email)
    is_verified = bcrypt.checkpw(log_info.pswd.encode(
        "utf-8"), user_to_log.pswd.encode("utf-8"))
    if not is_verified:
        return JSONResponse(status_code=400, content=dict(msg="Wrong password"))
    token = dict(
        Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(user_to_log).dict(), expires_delta=JWT_LOGIN_DELTA_TIME_MINUTE)}"
    )
    return token


async def create_user(session: AsyncSession, **kwargs):
    q = Users.insert().values(**kwargs)
    inserted_id = await session.execute(q)
    return inserted_id


async def get_hash_pswd(pswd: str):
    double_hash_object = hashlib.sha256()
    double_hash_object.update(pswd.encode("utf-8"))
    return double_hash_object.hexdigest()


async def is_email_exist(session: AsyncSession, email: str):
    q = Users.select().where(Users.c.email == email)
    get_email = await session.execute(q)
    if get_email.one_or_none():
        return get_email
    return False


async def is_phone_exist(session: AsyncSession, phone: str):
    q = Users.select().where(Users.c.phone == phone)
    get_phone = await session.execute(q)
    if get_phone.one_or_none():
        return get_phone
    return False
