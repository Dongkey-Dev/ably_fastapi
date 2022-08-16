import os
import re
from datetime import datetime
from typing import Optional

from pydantic import UUID4, root_validator
from pydantic.main import BaseModel
from pydantic.networks import EmailStr

CRYPTO_KEY = os.getenv("CRYPTO_KEY")


class UserRegistIn(BaseModel):
    email: EmailStr
    nickname: str
    username: str
    phone: str
    pswd: str
    confirm_pswd: str

    @root_validator
    def check_confirm_password(cls, values):
        password = values.get("pswd")
        confirm_password = values.get("confirm_pswd")
        if password != confirm_password:
            raise ValueError(
                "The password doesn't match with confirm_password")
        return values

    """
    If the client supports encryption...
    
    @validator('email', 'password', 'phone', 'username', pre=True)
    def decrypt_fields(cls, raw):
        aes = AESCipher(CRYPTO_KEY)
        try:
            dec = aes.decrypt(raw)
            dec[0]
        except Exception as e:
            raise ValueError("Invalid encryption.")
        return dec
    """


class ResetPswdIn(BaseModel):
    email: EmailStr
    pswd: str
    confirm_pswd: str

    @root_validator
    def check_confirm_password(cls, values):
        password = values.get("pswd")
        confirm_password = values.get("confirm_pswd")
        if password != confirm_password:
            raise ValueError(
                "The password doesn't match with confirm_password")
        return values


class MessageOut(BaseModel):
    msg: str


class ValidPhoneIn(BaseModel):
    username: str
    phone: str

    @root_validator
    def check_phone_number(cls, values):
        phone = values.get("phone")
        if not bool(re.search("[0-1]{2}\d{8,9}", phone)):
            raise ValueError(
                "Wrong phone number")
        return values


class UserPhoneToken(BaseModel):
    phone: str

    class Config:
        orm_mode = True


class UserPhonePswdToken(BaseModel):
    phone: str
    doublehash_pswd: str = None

    class Config:
        orm_mode = True


class UserToken(BaseModel):
    email: EmailStr = None

    class Config:
        orm_mode = True


class UserLoginIn(BaseModel):
    email: EmailStr = None
    pswd: str


class UserInquireOut(BaseModel):
    email: EmailStr
    nickname: str
    username: str
    phone: str


class UsersAllOut(BaseModel):
    id: UUID4
    email: EmailStr
    nickname: str
    username: str
    phone: str
    pswd: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class Token(BaseModel):
    Authorization: str = None

    class Config:
        orm_mode = True
