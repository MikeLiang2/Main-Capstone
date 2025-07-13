from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.models.users import UserInfo
from app.utils.auth import mock_user
from app.utils.token import get_current_user

router = APIRouter()
security = HTTPBearer()
# GET /user/info 获取用户信息
@router.get("/user/info", response_model=UserInfo)
def get_user_info(user=Depends(get_current_user)):
    return mock_user
