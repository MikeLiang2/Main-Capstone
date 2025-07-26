from typing import Optional
from uuid import UUID
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.db import get_async_session, User
from app.models.user import AccountInfo, UserRead, UserData, UserUpdate, UserPasswordUpdate
from app.auth.user_manager import require_permission, fastapi_users, UserManager, get_user_manager
from fastapi import Query
import re
from fastapi_users import models

router = APIRouter()


# PEOPLE_PERMISSIONS = [
#     "addPeople", "deletePeople", "editPeople", "editPassword"
# ]

# ROLE_PERMISSIONS = [
#     "addRole", "editRole"
# ]

# CHECKLIST_PERMISSIONS = [
#     "shareChecklist", "shareAnyChecklist",
#     "editChecklist", "editAnyChecklist",
#     "deleteChecklist", "deleteAnyChecklist",
#     "addChecklist"
# ]


# permission control
# get users with pagination and permission check
@router.get("/users", response_model=UserData)
async def get_users(
    page: int = 1,
    limit: int = 10,
    name: Optional[str] = Query(None),
    user=Depends(require_permission("editPeople")),
    db: AsyncSession = Depends(get_async_session),
):
    skip = (page - 1) * limit

    query = select(User)
    count_query = select(func.count()).select_from(User)

    if name:
        query = query.where(User.username.ilike(f"%{name}%"))
        count_query = count_query.where(User.username.ilike(f"%{name}%"))

    result = await db.execute(query.offset(skip).limit(limit))
    users = result.scalars().all()

    total = await db.scalar(count_query)

    return UserData(records=users, total=total)


# update user
@router.patch("/userstmp/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_async_session),
    user=Depends(require_permission(["editPeople"])),
):
    # get the user by ID
    result = await db.execute(select(User).where(User.id == user_id))
    target_user = result.scalar_one_or_none()

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_data.email is not None:
        target_user.email = user_data.email

    if user_data.username is not None:
        target_user.username = user_data.username

    if user_data.avatar is not None:
        target_user.avatar = user_data.avatar

    if user_data.roleId is not None:
        target_user.roleId = user_data.roleId

    try:
        await db.commit()
        await db.refresh(target_user)
        return target_user

    except IntegrityError as e:
        await db.rollback()

        err_msg = str(e.orig).lower()

        #  unique constraint error
        if "unique constraint" in err_msg or "duplicate key" in err_msg:
            # get the field name from the error message
            field = None
            match = re.search(r"key \((.*?)\)", err_msg)
            if match:
                field = match.group(1)
            detail_msg = f"{field.capitalize() if field else 'Field'} already exists"
            raise HTTPException(status_code=409, detail=detail_msg)

        elif "foreign key constraint" in err_msg:
            raise HTTPException(status_code=400, detail="Invalid foreign key reference")

        elif "value too long" in err_msg or "invalid input" in err_msg:
            raise HTTPException(status_code=422, detail="Invalid field value")

        else:
            raise HTTPException(status_code=500, detail="Unknown database error")


# remove user
@router.delete("/userstmp/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    user=Depends(require_permission(["deletePeople"])),
):
    result = await db.execute(select(User).where(User.id == user_id))
    target_user = result.scalar_one_or_none()

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    if str(user.id) == str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot delete your own account"
        )

    await db.delete(target_user)
    await db.commit()


@router.patch("/users/{user_id}/password", status_code=status.HTTP_200_OK)
async def admin_change_user_password(
    user_id: UUID,
    password_data: UserPasswordUpdate, 
    perm=Depends(require_permission(["editPassword"])),
    session: AsyncSession = Depends(get_async_session),
    manager: UserManager = Depends(get_user_manager)
):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = await manager.hash_password(password_data.password)

    await session.execute(
        update(User)
        .where(User.id == user_id)
        .values(hashed_password=hashed_password)
    )
    await session.commit()

    return {"message": "Password updated successfully"}
