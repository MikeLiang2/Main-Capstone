import uuid
from typing import List, Optional, Union

from fastapi import Depends, Request, HTTPException
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db import User, get_user_db, get_async_session

SECRET = "SECRET"


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    @property
    def requires_verification(self) -> bool:
        return False
    
    async def hash_password(self, password: str) -> str:
        return self.password_helper.hash(password)

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        user.roleId = 1
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy[models.UP, models.ID]:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])


current_active_user = fastapi_users.current_user(active=True)

# # premission checking for edit people
# async def get_edit_people_user(user: User = Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
#     await db.refresh(user, attribute_names=["role"])
#     if not user.role.editPeople:
#         raise HTTPException(
#             status_code=403,
#             detail="You do not have permission to access this resource.",
#         )
#     return user

#################################################################
# permission checking for specific actions
# usage: user=Depends(require_permission("editPeople"))

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

# # 单个权限
# Depends(require_permission("editPeople"))

# # 需要全部权限
# Depends(require_permission(["editPeople", "addPeople"], require_all=True))

# # 只要满足任意一个权限
# Depends(require_permission(["editPeople", "addPeople"], require_all=False))


def require_permission(permissions: Union[str, List[str]], require_all: bool = True):
    if isinstance(permissions, str):
        permissions = [permissions]

    async def dependency(
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session),
    ):
        await db.refresh(user, attribute_names=["role"])
        role = user.role

        if not role:
            raise HTTPException(status_code=403, detail="No role assigned to user.")

        # checjk if user has the required permissions
        results = [getattr(role, perm, False) for perm in permissions]

        if require_all:
            if not all(results):
                raise HTTPException(
                    status_code=403,
                    detail=f"Requires ALL of permissions: {permissions}",
                )
        else:
            if not any(results):
                raise HTTPException(
                    status_code=403,
                    detail=f"Requires AT LEAST ONE of permissions: {permissions}",
                )

        return user

    return dependency
