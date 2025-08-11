from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Query, Depends, status
from fastapi.responses import JSONResponse
from typing import List, Optional
from app.utils.checklist_access import build_checklist_query, has_any_global_permission
from app.auth.user_manager import require_permission
from app.models.db import (
    ProcessInstanceShare,
    User,
    get_async_session,
    ProcessInstance,
    ChecklistStage,
    ChecklistStep,
    ProcessInstanceShare,
    ProcessCategory,
)
from app.models.checklists import (
    ChecklistListResponse,
    ChecklistStageCreate,
    ProcessInstanceBase,
    ProcessInstanceCreate,
    ProcessInstanceBase,
    PromptRequest,
    ShareChecklistRequest,
    ProcessCategoryCreate,
    ProcessCategoryBase,
)
from uuid import UUID
from app.utils.vertex_ai import generate_checklist

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


@router.get("/checklist", response_model=ChecklistListResponse)
async def get_checklists(
    page: int = 1,
    limit: int = 10,
    name: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(
        require_permission(
            [
                "shareAnyChecklist",
                "editAnyChecklist",
                "deleteAnyChecklist",
                "shareChecklist",
                "editChecklist",
                "deleteChecklist",
            ],
            require_all=False,
        )
    ),
):
    offset = (page - 1) * limit

    stmt = build_checklist_query(user, name).offset(offset).limit(limit)
    result = await db.execute(stmt)
    orm_instances = result.scalars().all()

    # total count 同样使用权限过滤逻辑
    count_stmt = (
        build_checklist_query(user, name).with_only_columns(func.count()).order_by(None)
    )
    total_result = await db.execute(count_stmt)
    total = total_result.scalar()

    return ChecklistListResponse(records=orm_instances, total=total)


@router.get("/checklist/{process_id}", response_model=ProcessInstanceBase)
async def get_process_by_id(
    process_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(
        require_permission(
            [
                "shareAnyChecklist",
                "editAnyChecklist",
                "deleteAnyChecklist",
                "shareChecklist",
                "editChecklist",
                "deleteChecklist",
            ],
            require_all=False,
        )
    ),
):
    stmt = (
        select(ProcessInstance)
        .options(
            selectinload(ProcessInstance.category),
            selectinload(ProcessInstance.stages).selectinload(ChecklistStage.steps),
            selectinload(ProcessInstance.owner),
            selectinload(ProcessInstance.shared_users).selectinload(
                ProcessInstanceShare.user
            ),
        )
        .where(ProcessInstance.id == process_id)
    )

    result = await db.execute(stmt)
    process = result.scalar_one_or_none()
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    # if not has_any_global_permission(user):
    # must be owner or shared to check
    if not has_any_global_permission(user):
        if process.owner_id != user.id:
            shared_stmt = select(ProcessInstanceShare).where(
                ProcessInstanceShare.user_id == user.id,
                ProcessInstanceShare.process_id == process_id,
            )
            shared_result = await db.execute(shared_stmt)
            if not shared_result.scalar_one_or_none():
                raise HTTPException(
                    status_code=403, detail="Access denied to this checklist"
                )

    return process


@router.post("/checklist", response_model=ProcessInstanceBase)
async def create_process(
    process: ProcessInstanceCreate,
    db: AsyncSession = Depends(get_async_session),
    user=Depends(require_permission("addChecklist")),
):
    new_process = ProcessInstance(
        name=process.name,
        description=process.description,
        category_id=process.category_id,
        owner_id=user.id,
    )
    db.add(new_process)
    await db.flush()

    for stage_data in process.stages:
        new_stage = ChecklistStage(
            name=stage_data.name, order=stage_data.order, process_id=new_process.id
        )
        db.add(new_stage)
        await db.flush()

        for step_data in stage_data.steps:
            new_step = ChecklistStep(
                name=step_data.name,
                description=step_data.description,
                completed=step_data.completed,
                resourceUrl=step_data.resourceUrl,
                stage_id=new_stage.id,
            )
            db.add(new_step)

    await db.commit()

    # selectinload
    stmt = (
        select(ProcessInstance)
        .where(ProcessInstance.id == new_process.id)
        .options(
            selectinload(ProcessInstance.category),
            selectinload(ProcessInstance.stages).selectinload(ChecklistStage.steps),
            selectinload(ProcessInstance.owner),
            selectinload(ProcessInstance.shared_users).selectinload(
                ProcessInstanceShare.user
            ),
        )
    )
    result = await db.execute(stmt)
    full_process = result.scalar_one()

    return full_process


@router.put("/checklist/{process_id}", response_model=ProcessInstanceBase)
async def update_process(
    process_id: int,
    updated: ProcessInstanceCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(
        require_permission(
            [
                "editChecklist",
                "editAnyChecklist",
            ],
            require_all=False,
        )
    ),
):
    result = await db.execute(
        select(ProcessInstance).where(ProcessInstance.id == process_id)
    )
    target = result.scalar_one_or_none()

    if not target:
        raise HTTPException(status_code=404, detail="Process not found")

    # 权限校验：不是 owner，则需要有 editAny 或者被分享了且 can_edit
    if target.owner_id != user.id:
        role = user.role
        if not (
            role.editAnyChecklist or role.shareAnyChecklist or role.deleteAnyChecklist
        ):
            shared_result = await db.execute(
                select(ProcessInstanceShare).where(
                    ProcessInstanceShare.user_id == user.id,
                    ProcessInstanceShare.process_id == process_id,
                    ProcessInstanceShare.can_edit == True,
                )
            )
            if not shared_result.scalar_one_or_none():
                raise HTTPException(
                    status_code=403,
                    detail="You have no permission to edit this checklist",
                )

    # update process instance
    target.name = updated.name
    target.description = updated.description
    target.category_id = updated.category_id

    # remove old stage/step
    await db.execute(
        ChecklistStep.__table__.delete().where(
            ChecklistStep.stage_id.in_(
                select(ChecklistStage.id).where(ChecklistStage.process_id == process_id)
            )
        )
    )
    await db.execute(
        ChecklistStage.__table__.delete().where(ChecklistStage.process_id == process_id)
    )
    await db.flush()

    # add new stage/step
    for stage_data in updated.stages:
        new_stage = ChecklistStage(
            name=stage_data.name, order=stage_data.order, process_id=process_id
        )
        db.add(new_stage)
        await db.flush()

        for step_data in stage_data.steps:
            new_step = ChecklistStep(
                name=step_data.name,
                description=step_data.description,
                completed=step_data.completed,
                resourceUrl=step_data.resourceUrl,
                stage_id=new_stage.id,
            )
            db.add(new_step)

    await db.commit()

    # refresh and return the updated process
    stmt = (
        select(ProcessInstance)
        .where(ProcessInstance.id == process_id)
        .options(
            selectinload(ProcessInstance.category),
            selectinload(ProcessInstance.stages).selectinload(ChecklistStage.steps),
            selectinload(ProcessInstance.owner),
            selectinload(ProcessInstance.shared_users).selectinload(
                ProcessInstanceShare.user
            ),
        )
    )
    result = await db.execute(stmt)
    full_process = result.scalar_one()

    return full_process


@router.post("/category", response_model=ProcessCategoryCreate)
async def create_category(
    category: ProcessCategoryCreate,
    db: AsyncSession = Depends(get_async_session),
):
    new_category = ProcessCategory(name=category.name)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category


@router.get("/category", response_model=List[ProcessCategoryBase])
async def get_categories(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(ProcessCategory))
    return result.scalars().all()


# @router.delete("/checklist/{checklist_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_checklist(
#     checklist_id: int,
#     db: AsyncSession = Depends(get_async_session),
#     user=Depends(
#         require_permission(["deleteChecklist", "deleteAnyChecklist"], require_all=False)
#     ),
# ):
#     result = await db.execute(
#         select(ProcessInstance).where(ProcessInstance.id == checklist_id)
#     )
#     checklist = result.scalar_one_or_none()
#     if not checklist:
#         raise HTTPException(status_code=404, detail="Checklist not found")

#     await db.delete(checklist)
#     await db.commit()
#     return


@router.delete("/checklist/{checklist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_checklist(
    checklist_id: int,
    db: AsyncSession = Depends(get_async_session),
    user=Depends(
        require_permission(["deleteChecklist", "deleteAnyChecklist"], require_all=False)
    ),
):
    result = await db.execute(
        select(ProcessInstance).where(ProcessInstance.id == checklist_id)
    )
    checklist = result.scalar_one_or_none()
    if not checklist:
        raise HTTPException(status_code=404, detail="Checklist not found")

    # 权限判断：
    if checklist.owner_id == user.id:
        # 自己是 owner，允许删除
        pass
    elif user.role.deleteAnyChecklist:
        # 具备 deleteAnyChecklist 权限，允许删除
        pass
    else:
        # 检查是否是 shared 用户（但无权删除）
        shared_result = await db.execute(
            select(ProcessInstanceShare).where(
                ProcessInstanceShare.user_id == user.id,
                ProcessInstanceShare.process_id == checklist_id,
            )
        )
        shared = shared_result.scalar_one_or_none()
        if shared:
            raise HTTPException(
                status_code=403,
                detail="Shared users are not allowed to delete this checklist",
            )

        # 非 owner 且非管理员 且未被分享
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this checklist",
        )

    # 执行删除
    await db.delete(checklist)
    await db.commit()
    return


@router.post("/processes/{process_id}/share")
async def share_checklist(
    process_id: int,
    payload: ShareChecklistRequest,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(
        require_permission(
            [
                "shareAnyChecklist",
                "shareChecklist",
            ],
            require_all=False,
        )
    ),
):
    # search process
    result = await db.execute(
        select(ProcessInstance).where(ProcessInstance.id == process_id)
    )
    process = result.scalar_one_or_none()

    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    # premission check, 权限校验：必须是 owner 或具备 shareAnyChecklist 权限

    # permission check
    if process.owner_id != user.id:
        if user.role.shareAnyChecklist:
            pass  # allow
        else:
            # check if shared and has can_share permission
            shared_result = await db.execute(
                select(ProcessInstanceShare).where(
                    ProcessInstanceShare.user_id == user.id,
                    ProcessInstanceShare.process_id == process_id,
                    ProcessInstanceShare.can_share == True,
                )
            )
            if not shared_result.scalar_one_or_none():
                raise HTTPException(
                    status_code=403,
                    detail="You do not have permission to share this checklist",
                )

    # fine the target user
    result = await db.execute(select(User).where(User.email == payload.email))
    target_user = result.scalar_one_or_none()

    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")

    if user.id == target_user.id:
        raise HTTPException(status_code=400, detail="Cannot share to yourself")

    # prevent sharing to owner
    if target_user.id == process.owner_id:
        raise HTTPException(
            status_code=400, detail="Cannot share back to the checklist owner"
        )

    # check if already shared
    # exists = await db.execute(
    #     select(ProcessInstanceShare).where(
    #         ProcessInstanceShare.user_id == target_user.id,
    #         ProcessInstanceShare.process_id == process_id,
    #     )
    # )
    # if exists.scalar_one_or_none():
    #     raise HTTPException(status_code=400, detail="Already shared")

    existing_share_result = await db.execute(
        select(ProcessInstanceShare).where(
            ProcessInstanceShare.user_id == target_user.id,
            ProcessInstanceShare.process_id == process_id,
        )
    )
    existing_share = existing_share_result.scalar_one_or_none()

    #  owner or editAnyChecklist edit existing share
    if existing_share:
        if process.owner_id != user.id and not user.role.editAnyChecklist:
            raise HTTPException(
                status_code=403,
                detail="You cannot modify an existing share",
            )

        # if user is owner or has editAnyChecklist, update existing share
        # can_edit is only allowed if user is owner or has editAnyChecklist
        existing_share.can_edit = (
            payload.can_edit
            if process.owner_id == user.id or user.role.editAnyChecklist
            else False
        )
        existing_share.can_share = payload.can_share
        await db.commit()
        return {"message": "Existing share updated"}

    # insert share record
    can_edit = False
    if payload.can_edit:
        if process.owner_id == user.id or user.role.editAnyChecklist:
            can_edit = True
        else:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed to grant edit permission",
            )

    share = ProcessInstanceShare(
        user_id=target_user.id,
        process_id=process_id,
        can_edit=can_edit,
        can_share=payload.can_share,
    )
    db.add(share)
    await db.commit()

    return {"message": "Process shared successfully"}


@router.delete(
    "/processes/{process_id}/share/{target_user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_share(
    process_id: int,
    target_user_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(
        require_permission(
            [
                "shareAnyChecklist",
                "editAnyChecklist",
                "deleteAnyChecklist",
            ],
            require_all=False,
        )
    ),
):
    result = await db.execute(
        select(ProcessInstance).where(ProcessInstance.id == process_id)
    )
    process = result.scalar_one_or_none()

    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    if process.owner_id != user.id and not (
        user.role.shareAnyChecklist
        or user.role.editAnyChecklist
        or user.role.deleteAnyChecklist
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this share",
        )

    share_result = await db.execute(
        select(ProcessInstanceShare).where(
            ProcessInstanceShare.process_id == process_id,
            ProcessInstanceShare.user_id == target_user_id,
        )
    )
    share = share_result.scalar_one_or_none()
    if not share:
        raise HTTPException(status_code=404, detail="Share not found")

    await db.delete(share)
    await db.commit()
    return


# Copy checklist
@router.post("/checklist/{process_id}/copy", response_model=ProcessInstanceBase)
async def copy_checklist(
    process_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(require_permission(["addChecklist"], require_all=False)),
):
    # get original checklist
    result = await db.execute(
        select(ProcessInstance)
        .where(ProcessInstance.id == process_id)
        .options(
            selectinload(ProcessInstance.stages).selectinload(ChecklistStage.steps),
        )
    )
    original = result.scalar_one_or_none()

    if not original:
        raise HTTPException(status_code=404, detail="Original checklist not found")

    # create new checklist
    new_process = ProcessInstance(
        name=f"{original.name} (Copy)",
        description=original.description,
        category_id=original.category_id,
        owner_id=user.id,
    )
    db.add(new_process)
    await db.flush()  # generate new_process.id

    # copy stages and steps
    for stage in original.stages:
        new_stage = ChecklistStage(
            name=stage.name,
            order=stage.order,
            process_id=new_process.id,
        )
        db.add(new_stage)
        await db.flush()

        for step in stage.steps:
            new_step = ChecklistStep(
                name=step.name,
                description=step.description,
                completed=False,
                resourceUrl=step.resourceUrl,
                stage_id=new_stage.id,
            )
            db.add(new_step)

    await db.commit()

    # return complete object (including category and stage)
    result = await db.execute(
        select(ProcessInstance)
        .where(ProcessInstance.id == new_process.id)
        .options(
            selectinload(ProcessInstance.category),
            selectinload(ProcessInstance.stages).selectinload(ChecklistStage.steps),
            selectinload(ProcessInstance.owner),
            selectinload(ProcessInstance.shared_users).selectinload(
                ProcessInstanceShare.user
            ),
        )
    )
    return result.scalar_one()




@router.post("/checklist/generate", response_model=ProcessInstanceCreate)
async def generate_checklist_from_ai(payload: PromptRequest):
    try:
        process = generate_checklist(payload.prompt)
        return process
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": "AI response parse failed", "detail": str(e)},
        )