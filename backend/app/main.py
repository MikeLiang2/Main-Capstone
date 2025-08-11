from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users.db import SQLAlchemyUserDatabase
from app.routers import checklist, role, users
from app.models.user import UserCreate, UserRead, UserUpdate
from app.auth.user_manager import auth_backend, fastapi_users, get_user_manager
from app.models.db import async_session_maker, User
from app.seed.seed import wait_for_db, wait_for_migrations_to_complete, seed_roles, seed_categories, seed_users

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(users.router)
app.include_router(checklist.router)
# app.include_router(premission.router)
app.include_router(role.router)

# allow CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Checklist System"}


@app.on_event("startup")
async def startup_event():
    await wait_for_db()

    async with async_session_maker() as session:
        await wait_for_migrations_to_complete(session)
        await seed_roles(session)
        await seed_categories(session)
        await seed_users(session, await anext(get_user_manager(SQLAlchemyUserDatabase(session, User))))
