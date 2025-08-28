from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.avatar_service import generate_avatar, approve_avatar
from app.models.db import get_async_session, User
from app.auth.user_manager import current_active_user

router = APIRouter(prefix="/avatar", tags=["Avatar"])


class AvatarPrompt(BaseModel):
    prompt: str
    style: str


class ApproveRequest(BaseModel):
    temp_url: str


class URLresponse(BaseModel):
    url: str


@router.post("/generate", response_model=URLresponse)
def generate_avatar_endpoint(data: AvatarPrompt, user: User = Depends(current_active_user)):
    try:
        temp_url = generate_avatar(data.prompt, data.style if data.style in [
                                   "vivid", "natural"] else "vivid")
        return URLresponse(url=temp_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/approve", response_model=URLresponse)
async def approve_avatar_endpoint(
    data: ApproveRequest,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    try:
        if user.avatar != data.temp_url:
            user.avatar = approve_avatar(data.temp_url, user.id, user.avatar)
            await db.commit()
            await db.refresh(user)

        return URLresponse(url=user.avatar)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
