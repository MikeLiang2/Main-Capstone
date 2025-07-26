from datetime import datetime
from sqlite3 import IntegrityError
from sqlalchemy import select, func, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.user_manager import require_permission
from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import Optional
import asyncpg

from app.models.db import get_async_session, Role as RoleModel, User
from app.models.role import Role as RoleSchema, RoleCreate, RoleList

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


# // Get roles with pagination and optional search by name
@router.get("/role", response_model=RoleList)
async def get_role_list_with_search(
    page: int = Query(1, gt=0),
    limit: int = Query(10, gt=0),
    name: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_async_session),
):
    skip = (page - 1) * limit

    query = select(RoleModel)
    if name:
        query = query.where(RoleModel.name.ilike(f"%{name}%"))

    total_query = select(func.count()).select_from(RoleModel)
    if name:
        total_query = total_query.where(RoleModel.name.ilike(f"%{name}%"))

    result = await db.execute(query.offset(skip).limit(limit))
    roles = result.scalars().all()

    total = await db.scalar(total_query)

    roles_data = [
        RoleSchema.model_validate(role, from_attributes=True) for role in roles
    ]

    return RoleList(roles=roles_data, total=total)


# // Get all roles
@router.get("/roles", response_model=list[RoleSchema])
async def get_all_roles(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(RoleModel))
    roles = result.scalars().all()
    return [RoleSchema.model_validate(role, from_attributes=True) for role in roles]


# // Create a new role
@router.post("/role", status_code=status.HTTP_201_CREATED)
async def create_role(
    role: RoleCreate,
    db: AsyncSession = Depends(get_async_session),
    user=Depends(require_permission("addRole")),
):
    # Check if the role with the same name exists
    result = await db.execute(select(RoleModel).where(RoleModel.name == role.name))
    existing_role = result.scalar_one_or_none()

    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Role name already exists"
        )

    stmt = insert(RoleModel).values(**role.dict())
    await db.execute(stmt)
    await db.commit()

    return {"message": "Role created"}


@router.put("/role/{role_id}", response_model=RoleSchema)
async def update_role(
    role_id: int,
    role_update: RoleCreate,
    user: User = Depends(require_permission("editRole")),
    db: AsyncSession = Depends(get_async_session),
):
    result = await db.execute(select(RoleModel).where(RoleModel.id == role_id))
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    for field, value in role_update.dict().items():
        setattr(role, field, value)
    await db.commit()
    await db.refresh(role)
    return role


@router.delete("/role/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(require_permission("editRole"))
):
    result = await db.execute(select(RoleModel).where(RoleModel.id == role_id))
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    await db.delete(role)
    await db.commit()
