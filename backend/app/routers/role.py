from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.role import Role, RoleList
from app.utils.roles import mock_roles
from app.utils.users import mock_users
from app.models.role import AssignedRole

router = APIRouter()

@router.get("/roles", response_model=RoleList)
def get_all_roles():
    return RoleList(roles=[Role(**role) for role in mock_roles])

@router.post("/roles/assign")
def assign_role(data: AssignedRole):
    user = next((u for u in mock_users if u["id"] == data.userId), None)
    role = next((r for r in mock_roles if r["id"] == data.roleId), None)

    if not user or not role:
        raise HTTPException(status_code=404, detail="User or role not found")

    user["roleId"] = role["id"]
    user["updateTime"] = datetime.now().isoformat()

    return {
        "message": "Role assigned successfully",
        "user": user
    }