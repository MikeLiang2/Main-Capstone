from typing import Optional
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db import ProcessInstance, ProcessInstanceShare, ChecklistStage, User

def has_any_global_permission(user: User) -> bool:
    role = user.role
    return role.shareAnyChecklist or role.editAnyChecklist or role.deleteAnyChecklist


def build_checklist_query(user: User, name: Optional[str] = None):
    base_stmt = select(ProcessInstance).options(
        selectinload(ProcessInstance.category),
        selectinload(ProcessInstance.stages).selectinload(ChecklistStage.steps),
        selectinload(ProcessInstance.owner),
        selectinload(ProcessInstance.shared_users).selectinload(
            ProcessInstanceShare.user
        ),
    )

    if has_any_global_permission(user):
        if name:
            base_stmt = base_stmt.where(ProcessInstance.name.ilike(f"%{name}%"))
        return base_stmt

    # owner or shared
    stmt = base_stmt.where(
        or_(
            ProcessInstance.owner_id == user.id,
            ProcessInstance.id.in_(
                select(ProcessInstanceShare.process_id).where(ProcessInstanceShare.user_id == user.id)
            )
        )
    )

    if name:
        stmt = stmt.where(ProcessInstance.name.ilike(f"%{name}%"))

    return stmt
