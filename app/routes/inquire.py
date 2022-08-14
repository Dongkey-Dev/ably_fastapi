from typing import List

from app.db.dbconn import db
from app.middleware.jwt_handler import get_user_token
from app.models import UserInquireOut, UsersAllOut
from app.utils.open_api_docs import auth_scheme
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/me", response_model=UserInquireOut, dependencies=[Depends(auth_scheme)])
async def read_users_me(user_info: UserInquireOut = Depends(get_user_token)):
    return user_info


@router.get("/get_all_users", response_model=List[UsersAllOut])
async def read_all_users_info_no_need_token():
    query = "select * from users"
    user_range = db.engine.execute(statement=query).yield_per(1)
    result = []
    for user_info in user_range:
        user_map = {}
        user_map["id"] = user_info[0]
        user_map["email"] = user_info[1]
        user_map["nickname"] = user_info[2]
        user_map["username"] = user_info[3]
        user_map["phone"] = user_info[4]
        user_map["pswd"] = user_info[5]
        user_map["created_at"] = user_info[6]
        user_map["updated_at"] = user_info[7]
        result.append(user_map)
    return result
