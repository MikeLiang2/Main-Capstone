from typing import List, Optional
from pydantic import BaseModel

from fastapi_users import schemas
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserRead(schemas.BaseUser[UUID]):
    username: str
    avatar: str
    roleId: int
    createTime: datetime
    updateTime: datetime

class UserCreate(schemas.BaseUserCreate):
    username: str
    avatar: str
    roleId: int

class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    avatar: Optional[str] = None
    roleId: Optional[int] = None


# Define the user info model for the response, st2
# 登陆用
class UserInfo(BaseModel):
    id: int
    avatar: str
    username: str
    password: str
    email: str
    token: str

# Define the request model for login, st1
class LoginRequest(BaseModel):
    username: str
    password: str

######################################

class UserSignUpRequest(BaseModel):
    username: str
    password: str
    email: str

#paging account info, 用户信息相关
class AccountInfo(BaseModel):
    id: Optional[int] = None
    createTime: str
    updateTime: str
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    roleId: Optional[int] = None


class UserData(BaseModel):
    records: List[AccountInfo]
    total: int

