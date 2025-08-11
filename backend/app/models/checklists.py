from pydantic import BaseModel, EmailStr
from typing import List, Optional

from uuid import UUID

class UserBrief(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    avatar: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class ProcessShareRead(BaseModel):
    user: UserBrief
    can_edit: bool
    can_share: bool

    model_config = {
        "from_attributes": True
    }

class ChecklistStepBase(BaseModel):
    id: int
    name: str
    description: str
    completed: bool
    resourceUrl: str
    model_config = {
        "from_attributes": True
    }

class ChecklistStageBase(BaseModel):
    id: int
    name: str
    order: int
    steps: List[ChecklistStepBase]
    model_config = {
        "from_attributes": True
    }

class ProcessCategoryBase(BaseModel):
    id: int
    name: str
    model_config = {
        "from_attributes": True
    }

class ProcessInstanceBase(BaseModel):
    id: int
    name: str
    description: str
    category: ProcessCategoryBase
    stages: List[ChecklistStageBase]
    owner: UserBrief
    shared_users: List[ProcessShareRead]
    model_config = {
        "from_attributes": True
    }

###############

class ChecklistStepCreate(BaseModel):
    name: str
    description: str
    completed: bool = False
    resourceUrl: str

class ChecklistStageCreate(BaseModel):
    name: str
    order: int
    steps: List[ChecklistStepCreate]

class ProcessInstanceCreate(BaseModel):
    name: str
    description: str
    category_id: int
    stages: List[ChecklistStageCreate]


class ProcessCategoryCreate(BaseModel):
    name: str

#####################
class ChecklistListResponse(BaseModel):
    records: List[ProcessInstanceBase]
    total: int

    model_config = {
        "from_attributes": True
    }


class ChecklistStepRead(BaseModel):
    id: int
    name: str
    completed: bool

    model_config = {
        "from_attributes": True
    }
class ChecklistStageRead(BaseModel):
    id: int
    name: str
    steps: List[ChecklistStepRead]

    model_config = {
        "from_attributes": True
    }

class CategoryRead(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

class ChecklistRead(BaseModel):
    id: int
    name: str
    category: CategoryRead
    stages: List[ChecklistStageRead]

    model_config = {
        "from_attributes": True
    }


class ShareChecklistRequest(BaseModel):
    email: EmailStr
    can_edit: Optional[bool] = False
    can_share: Optional[bool] = False


class PromptRequest(BaseModel):
    prompt: str