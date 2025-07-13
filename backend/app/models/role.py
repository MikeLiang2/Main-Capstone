from typing import List, Optional

from pydantic import BaseModel


class Role(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class RoleList(BaseModel):
    roles: List[Role]
    
class AssignedRole(BaseModel):
    userId: int
    roleId: int