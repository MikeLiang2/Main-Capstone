from collections.abc import AsyncGenerator
import os
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import String, DateTime, ForeignKey, Column, Integer, String, Boolean, CheckConstraint

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

    roleId = Column(Integer, ForeignKey("roles.id"), nullable=False, default=1)
    # many - one relationship
    role = relationship("Role", back_populates="users")

    created_processes = relationship("ProcessInstance", back_populates="owner", cascade="all, delete-orphan")
    shared_processes = relationship("ProcessInstanceShare", back_populates="user", cascade="all, delete-orphan")

    createTime = Column(DateTime, default=datetime.utcnow, nullable=True)
    updateTime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)


class Role(Base):   
    __tablename__ = "roles"
    users = relationship("User", back_populates="role")

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    # People permissions
    addPeople = Column(Boolean, default=False)
    deletePeople = Column(Boolean, default=False)
    editPeople = Column(Boolean, default=False)
    editPassword = Column(Boolean, default=False)

    # Role permissions
    addRole = Column(Boolean, default=False)
    editRole = Column(Boolean, default=False)

    # Checklist permissions
    shareChecklist = Column(Boolean, default=False)
    shareAnyChecklist = Column(Boolean, default=False)
    editChecklist = Column(Boolean, default=False)
    editAnyChecklist = Column(Boolean, default=False)
    deleteChecklist = Column(Boolean, default=False)
    deleteAnyChecklist = Column(Boolean, default=False)
    addChecklist = Column(Boolean, default=False)

    createTime = Column(DateTime, default=datetime.utcnow, nullable=True)
    updateTime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)


class ProcessCategory(Base):
    __tablename__ = "process_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    processes = relationship("ProcessInstance", back_populates="category")


class ProcessInstance(Base):
    __tablename__ = "processes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)

    category_id = Column(Integer, ForeignKey("process_categories.id"))
    category = relationship("ProcessCategory", back_populates="processes")

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="created_processes")

    shared_users = relationship("ProcessInstanceShare", back_populates="process", cascade="all, delete-orphan")

    stages = relationship("ChecklistStage", back_populates="process", cascade="all, delete")


class ChecklistStage(Base):
    __tablename__ = "stages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    order = Column(Integer)

    process_id = Column(Integer, ForeignKey("processes.id"))
    process = relationship("ProcessInstance", back_populates="stages")

    steps = relationship("ChecklistStep", back_populates="stage", cascade="all, delete")


class ChecklistStep(Base):
    __tablename__ = "steps"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
    resourceUrl = Column(String)

    stage_id = Column(Integer, ForeignKey("stages.id"))
    stage = relationship("ChecklistStage", back_populates="steps")


class ProcessInstanceShare(Base):
    __tablename__ = "process_instance_shares"
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    process_id = Column(Integer, ForeignKey("processes.id"))

    can_edit = Column(Boolean, default=False)
    can_share = Column(Boolean, default=False)

    user = relationship("User", back_populates="shared_processes")
    process = relationship("ProcessInstance", back_populates="shared_users")