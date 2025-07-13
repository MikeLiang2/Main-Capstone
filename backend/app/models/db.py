from collections.abc import AsyncGenerator
import os
from datetime import datetime
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, DateTime, ForeignKey, Column, Integer, String, Boolean

# DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/checklist"
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    username = Column(String, index=True, nullable=False)
    avatar = Column(String, index=True, nullable=True)

    roleId = Column(Integer, index=True, nullable=False)

    createTime = Column(DateTime, default=datetime.utcnow, nullable=True)
    updateTime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)