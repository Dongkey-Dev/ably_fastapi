from datetime import datetime, timedelta

from app.common.consts import JWT_ALGORITHM, JWT_SECRET
from app.db.schema import Users
from app.models import (UserInquireOut, UserPhonePswdToken, UserPhoneToken,
                        UserToken)
from app.utils.query_utils import to_dict
from fastapi import Depends, HTTPException, Request, status

import jwt


def getHTTPException(msg):
    exce = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"{msg}",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return exce


credentials_exception = getHTTPException("Invalid credentials token")
invalid_phone_match_exception = getHTTPException(
    "Token, phone are not matched.")


async def jwt_call(request: Request):
    authorization: str = request.headers.get("Authorization")
    authorization = authorization.replace("Bearer", "").strip()
    if not authorization:
        raise HTTPException(
            status_code="403", detail="Not authenticated"
        )
    return authorization


async def jwt_decode(token: str):
    token_data = token.replace('Bearer', '').strip()
    payload = jwt.decode(token_data, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return payload


async def valid_token(token: str = Depends(jwt_call)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except Exception as e:
        raise credentials_exception
    return payload


async def get_phone_token(payload: dict = Depends(valid_token)):
    phone: str = payload.get("phone")
    try:
        if phone is None:
            raise credentials_exception
        token_data = UserPhoneToken(phone=phone)
    except Exception as e:
        raise credentials_exception
    return token_data


async def get_phone_hashpswd_token(payload: dict = Depends(valid_token)):
    try:
        phone: str = payload.get("phone")
        doublehash_pswd: str = payload.get("doublehash_pswd")
        if phone is None or doublehash_pswd is None:
            raise credentials_exception
        token_data = UserPhonePswdToken(
            phone=phone, doublehash_pswd=doublehash_pswd)
    except Exception as e:
        raise credentials_exception
    return token_data


async def get_user_token(payload: dict = Depends(valid_token)):
    email: str = payload.get("email")
    try:
        if email is None:
            raise credentials_exception
        token_data = UserToken(email=email)
    except Exception as e:
        raise credentials_exception
    user = Users.get(email=token_data.email)
    if user is None:
        raise credentials_exception
    user_dict = to_dict(user)
    user_out = UserInquireOut(**user_dict)
    return user_out


def create_access_token(*, data: dict = None, expires_delta: int):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() +
                         timedelta(minutes=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt
