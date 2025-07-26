from typing import List, Optional
from pydantic import BaseModel

class Role(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    addPeople: bool
    deletePeople: bool
    editPeople: bool
    editPassword: bool
    addRole: bool
    editRole: bool
    shareChecklist: bool
    shareAnyChecklist: bool
    editChecklist: bool
    editAnyChecklist: bool
    deleteChecklist: bool
    deleteAnyChecklist: bool
    addChecklist: bool

    class Config:
        from_attributes = True

class RoleList(BaseModel):
    roles: List[Role]
    total: int


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    
    addPeople: bool = False
    deletePeople: bool = False
    editPeople: bool = False
    editPassword: bool = False
    addRole: bool = False
    editRole: bool = False
    shareChecklist: bool = False
    shareAnyChecklist: bool = False
    editChecklist: bool = False
    editAnyChecklist: bool = False
    deleteChecklist: bool = False
    deleteAnyChecklist: bool = False
    addChecklist: bool = False