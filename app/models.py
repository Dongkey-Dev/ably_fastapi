import os
from pydantic import root_validator, validator
from pydantic.main import BaseModel
from pydantic.networks import EmailStr
from crypto.cipher import AESCipher

CRYPTO_KEY = os.getenv("CRYPTO_KEY")

class UserRegistIn(BaseModel):
    email : EmailStr
    nickname : str
    username : str
    phone : str
    pswd : str
    confirm_pswd : str
    
    @root_validator
    def check_confirm_password(cls, values):
        password = values.get("pswd")
        confirm_password = values.get("confirm_pswd")
        if password != confirm_password:
            raise ValueError("The password doesn't match with confirm_password")
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
    email : EmailStr
    pswd : str
    confirm_pswd : str    
    
    @root_validator
    def check_confirm_password(cls, values):
        password = values.get("pswd")
        confirm_password = values.get("confirm_pswd")
        if password != confirm_password:
            raise ValueError("The password doesn't match with confirm_password")
        return values    
    
class MessageOut(BaseModel):
    msg : str    
    
class ValidPhoneIn(BaseModel):
    username : str
    phone : str
    
class UserPhoneToken(BaseModel):
    phone: str = None
    class Config:
        orm_mode = True   
        
class UserPhonePswdToken(BaseModel):
    phone: str = None
    doublehash_pswd: str = None
    class Config:
        orm_mode = True                
    
class UserToken(BaseModel):
    email: EmailStr = None
    class Config:
        orm_mode = True    
    
class UserLoginIn(BaseModel):
    email : EmailStr = None
    pswd : str
    
class UserInquireOut(BaseModel):
    email : EmailStr
    nickname : str    
    username : str
    phone : str

class Token(BaseModel):
    Authorization: str = None
    class Config:
        orm_mode = True      