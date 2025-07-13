from fastapi import APIRouter, HTTPException
from app.models.users import LoginRequest
from app.utils.auth import mock_user
from app.utils.token import create_access_token
from datetime import timedelta

router = APIRouter() 

# POST /login endpoint for user login
@router.post("/login")
def login(data: LoginRequest):
    if data.username == mock_user.username and data.password == mock_user.password:
        token = create_access_token(
            data={"sub": data.username},
            expires_delta=timedelta(minutes=30)
        )
        return {
            "token": token
        }
    else: 
        raise HTTPException(status_code=401, detail="Username or password is incorrect")