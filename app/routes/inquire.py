from typing import List

from app.db.dbconn import db
from app.db.schema import UsersTable
from app.jwt.jwt_handler import get_user_token
from app.models import UserInquireOut, UsersAllOut
from app.utils.open_api_docs import auth_scheme
from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/me", response_model=UserInquireOut, dependencies=[Depends(auth_scheme)])
async def read_users_me(user_info: UserInquireOut = Depends(get_user_token)):
    return user_info


@router.get("/users", response_model=List[UsersAllOut])
async def read_all_users_info_no_need_token(session: AsyncSession = Depends(db.get_db_session)):
    q = UsersTable.select()
    users = await session.execute(q)
    return users.fetchall()
