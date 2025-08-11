import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select, text
from sqlalchemy.exc import ProgrammingError, OperationalError
from app.models.db import DATABASE_URL, ProcessCategory, Role, User
from datetime import datetime
from app.auth.user_manager import UserManager
from uuid import uuid4

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

mock_users = [
    {
        "id": uuid4(),
        "username": "qp",
        "avatar": "https://avatars.githubusercontent.com/u/91029359?v=4",
        "roleId": 2,
        "email": "qp@example.com",
        "password": "pass",
    }
]


REQUIRED_TABLES = [
    "roles",
    "process_categories",
    "users",
]


async def wait_for_db(timeout: int = 30):
    engine = create_async_engine(DATABASE_URL, echo=False)
    start = asyncio.get_event_loop().time()
    while True:
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            break
        except OperationalError:
            if asyncio.get_event_loop().time() - start > timeout:
                raise TimeoutError("Database not ready after waiting")
            await asyncio.sleep(1)
    await engine.dispose()


async def wait_for_migrations_to_complete(session: AsyncSession):
    retries = 10
    for i in range(retries):
        try:
            result = await session.execute(
                text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                """)
            )
            tables = set(row[0] for row in result.all())
            if all(t in tables for t in REQUIRED_TABLES):
                print("All required tables found. Proceeding with seeding.")
                return
            else:
                print(
                    f"Waiting for migration to create required tables... Attempt {i+1}/{retries}")
        except ProgrammingError:
            print(f"Could not check tables yet (attempt {i+1}/{retries})")
        await asyncio.sleep(2)
    raise RuntimeError(
        "Migrations did not complete in time. Backend startup aborted.")


async def seed_roles(session: AsyncSession):
    existing = await session.execute(select(Role.id))
    existing_ids = set(existing.scalars().all())

    roles_to_add = []
    for role in mock_roles:
        if role["id"] not in existing_ids:
            roles_to_add.append(
                Role(**role, createTime=datetime.utcnow(),
                     updateTime=datetime.utcnow())
            )

    if roles_to_add:
        session.add_all(roles_to_add)
        await session.commit()
        await session.execute(
            text(
                "SELECT setval(pg_get_serial_sequence('roles', 'id'), (SELECT MAX(id) FROM roles))"
            )
        )


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
        await session.execute(
            text(
                "SELECT setval(pg_get_serial_sequence('process_categories', 'id'), (SELECT MAX(id) FROM process_categories))"
            )
        )


async def seed_users(session: AsyncSession, manager: UserManager):
    existing_users_result = await session.execute(select(User.email))
    existing_emails = set(existing_users_result.scalars().all())

    for user_data in mock_users:
        if user_data["email"] in existing_emails:
            continue

        hashed_password = await manager.hash_password(user_data.pop("password"))

        user = User(
            **user_data,
            hashed_password=hashed_password,
            is_active=True,
            is_verified=True,
            is_superuser=False,
        )
        session.add(user)

    await session.commit()
