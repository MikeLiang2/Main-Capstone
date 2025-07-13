from pydantic import BaseModel
from typing import List
###############################
# Define checklist and process models, st3

class ChecklistStep(BaseModel):
    id: int
    name: str
    description: str
    completed: bool
    resourceUrl: str

class ChecklistStage(BaseModel):
    id: int
    name: str
    order: int
    steps: list[ChecklistStep]

class ProcessCategory(BaseModel):
    id: int
    name: str

class ProcessInstance(BaseModel):
    id: int
    name: str
    description: str
    category: ProcessCategory
    stages: List[ChecklistStage]

