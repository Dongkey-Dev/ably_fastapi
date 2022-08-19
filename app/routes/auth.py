import bcrypt
from app.common.consts import (JWT_LOGIN_DELTA_TIME_MINUTE,
                               JWT_REGIST_DELTA_TIME_MINUTE)
from app.db.dbconn import db
from app.jwt.jwt_handler import (create_access_token, get_phone_hashpswd_token,
                                 get_phone_token)
from app.models import (MessageOut, ResetPswdIn, Token, UserLoginIn,
                        UserPhonePswdToken, UserPhoneToken, UserRegistIn,
                        UserToken, ValidPhoneIn)
from app.utils import query_utils as qu
from app.utils.open_api_docs import auth_scheme
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

router = APIRouter()


@router.post("/auth/verify_phone_to_regist", status_code=202, response_model=Token)
async def verify_phone_to_regist(phone_info: ValidPhoneIn, session: AsyncSession = Depends(db.get_db_session)):
    is_exist = await qu.is_phone_exist(session, phone_info.phone)
    if is_exist:
        return JSONResponse(status_code=400, content=dict(msg="Already registered phone number."))
    data = UserPhoneToken.from_orm(phone_info).dict()
    token = dict(
        Authorization=f"Bearer {create_access_token(data=data, expires_delta=JWT_REGIST_DELTA_TIME_MINUTE)}"
    )
    return token


@router.post("/auth/user", status_code=201, response_model=MessageOut, dependencies=[Depends(auth_scheme)])
async def regist_user(reg_info: UserRegistIn, session=Depends(db.get_db_session), token_data=Depends(get_phone_token)):
    is_exist = await qu.is_email_exist(session, reg_info.email)
    if reg_info.phone != token_data.phone:
        return JSONResponse(status_code=400, content=dict(msg="The wrong phone number."))
    if is_exist:
        return JSONResponse(status_code=400, content=dict(msg="Email already exists."))
    hashed_pswd = bcrypt.hashpw(
        reg_info.pswd.encode("utf-8"), bcrypt.gensalt())
    await qu.create_user(session, email=reg_info.email, pswd=hashed_pswd.decode(),
                         nickname=reg_info.nickname, phone=reg_info.phone, username=reg_info.username)
    await session.commit()
    return MessageOut(msg=f"{reg_info.email} regist success.")


@router.post("/auth/verify_phone_to_reset_pswd", status_code=202, response_model=Token)
async def verify_phone_to_reset_pswd(phone_info: ValidPhoneIn, session=Depends(db.get_db_session)):
    user_to_reset = await qu.is_phone_exist(session, phone_info.phone)
    if not user_to_reset:
        return JSONResponse(status_code=400, content=dict(msg="There is no match user"))
    user_pswd = user_to_reset.pswd
    doublehash_pswd = await qu.get_hash_pswd(user_pswd)
    token_data = UserPhonePswdToken(
        phone=phone_info.phone, doublehash_pswd=doublehash_pswd)
    data = UserPhonePswdToken.from_orm(token_data).dict()
    token = dict(
        Authorization=f"Bearer {create_access_token(data=data, expires_delta=JWT_REGIST_DELTA_TIME_MINUTE)}"
    )
    return token


@router.put("/auth/user", status_code=201, response_model=MessageOut, dependencies=[Depends(auth_scheme)])
async def reset_pswd(reset_info: ResetPswdIn, phone_pswd_token=Depends(get_phone_hashpswd_token), session=Depends(db.get_db_session)):
    user_to_reset_pswd = await qu.is_email_exist(session, reset_info.email)
    doublehash_pswd = await qu.get_hash_pswd(user_to_reset_pswd.pswd)
    if not user_to_reset_pswd:
        return JSONResponse(status_code=400, content=dict(msg="There is no match user."))
    if phone_pswd_token.doublehash_pswd != doublehash_pswd:
        return JSONResponse(status_code=400, content=dict(msg="Looks like already reset password or wrong email."))
    hashed_pswd = bcrypt.hashpw(
        reset_info.pswd.encode("utf-8"), bcrypt.gensalt())
    await qu.update_user(
        session, user_to_reset_pswd.email, pswd=hashed_pswd.decode())
    await session.commit()
    return MessageOut(msg=f"{user_to_reset_pswd.email} password updated.")


@router.post("/auth/login", status_code=202, response_model=Token)
async def login_to_get_token_which_can_call_api_me(log_info: UserLoginIn, session=Depends(db.get_db_session)):
    is_exist = await qu.is_email_exist(session, log_info.email)
    if not is_exist:
        return JSONResponse(status_code=400, content=dict(msg="There is no match user"))
    user_to_log = await qu.is_email_exist(session, email=log_info.email)
    is_verified = bcrypt.checkpw(log_info.pswd.encode(
        "utf-8"), user_to_log.pswd.encode("utf-8"))
    if not is_verified:
        return JSONResponse(status_code=400, content=dict(msg="Wrong password"))
    data = UserToken.from_orm(user_to_log).dict()
    token = dict(
        Authorization=f"Bearer {create_access_token(data=data, expires_delta=JWT_LOGIN_DELTA_TIME_MINUTE)}"
    )
    return token
