from fastapi import APIRouter, HTTPException
from app.models.checklists import ChecklistStage, ChecklistStep, ProcessInstance
from typing import List
from app.utils.clmock import fake_stages, fake_checklist_data

router = APIRouter()

# 获取所有流程列表（不含阶段详情）
@router.get("/checklist", response_model=list[ProcessInstance])
def get_all_processes():
    return list(fake_checklist_data.values())

# 获取指定流程（含完整信息）
@router.get("/checklist/{process_id}", response_model=ProcessInstance)
def get_process_by_id(process_id: int):
    if process_id in fake_checklist_data:
        return fake_checklist_data[process_id]
    raise HTTPException(status_code=404, detail="Process not found")

# 更新流程（含 stages）
@router.put("/checklist/{process_id}", response_model=ProcessInstance)
def update_process(process_id: int, updated: ProcessInstance):
    if process_id not in fake_checklist_data:
        raise HTTPException(status_code=404, detail="Process not found")
    fake_checklist_data[process_id] = updated
    return updated

@router.post("/checklist")
def create_process(process: ProcessInstance):
    return {"message": "Process created", "process": process}
