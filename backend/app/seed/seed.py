from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.db import ProcessCategory, Role
from datetime import datetime

# predefined data to db
mock_roles = [
    {
        "id": 1,
        "name": "user",
        "description": "Regular User",
        "addPeople": False,
        "deletePeople": False,
        "editPeople": False,
        "editPassword": False,
        "addRole": False,
        "editRole": False,
        "shareChecklist": True,
        "shareAnyChecklist": False,
        "editChecklist": True,
        "editAnyChecklist": False,
        "deleteChecklist": True,
        "deleteAnyChecklist": False,
        "addChecklist": True,
    },
    {
        "id": 2,
        "name": "admin",
        "description": "Administrator",
        "addPeople": True,
        "deletePeople": True,
        "editPeople": True,
        "editPassword": True,
        "addRole": True,
        "editRole": True,
        "shareChecklist": True,
        "shareAnyChecklist": True,
        "editChecklist": True,
        "editAnyChecklist": True,
        "deleteChecklist": True,
        "deleteAnyChecklist": True,
        "addChecklist": True,
    },
    {
        "id": 3,
        "name": "manager",
        "description": "Manager",
        "addPeople": False,
        "deletePeople": False,
        "editPeople": False,
        "editPassword": False,
        "addRole": False,
        "editRole": False,
        "shareChecklist": True,
        "shareAnyChecklist": True,
        "editChecklist": True,
        "editAnyChecklist": True,
        "deleteChecklist": True,
        "deleteAnyChecklist": True,
        "addChecklist": True,
    },
]

mock_categories = [{"id": 1, "name": "General"}, {"id": 2, "name": "VISA"}]


async def seed_roles(session: AsyncSession):
    existing = await session.execute(select(Role.id))
    # existing_ids = {r.id for r in existing.scalars().all()}
    existing_ids = set(existing.scalars().all())

    roles_to_add = []
    for role in mock_roles:
        if role["id"] not in existing_ids:
            roles_to_add.append(
                Role(**role, createTime=datetime.utcnow(), updateTime=datetime.utcnow())
            )

    if roles_to_add:
        session.add_all(roles_to_add)
        await session.commit()

async def seed_categories(session: AsyncSession):
    existing_cats = await session.execute(select(ProcessCategory.id))
    existing_cat_ids = set(existing_cats.scalars().all())

    cats_to_add = []
    for cat in mock_categories:
        if cat["id"] not in existing_cat_ids:
            cats_to_add.append(ProcessCategory(**cat))

    if cats_to_add:
        session.add_all(cats_to_add)
        await session.commit()
