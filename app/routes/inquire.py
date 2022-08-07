from app.models import UserInquireOut
from fastapi import APIRouter, Depends
from app.middleware.jwt_handler import get_user_token
from app.utils.open_api_docs import auth_scheme

router = APIRouter()

@router.get("/me", response_model=UserInquireOut, dependencies=[Depends(auth_scheme)])
async def read_users_me(user_info: UserInquireOut = Depends(get_user_token)):
    return user_info