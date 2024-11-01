from pydantic import BaseModel, field_validator
from typing import Literal
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from database import Base


class TaskCreate(BaseModel):
    task_name: str
    status: Literal["active", "completed"]

    @field_validator('task_name')
    def task_name_must_not_be_empty(self, value):
        if not value.strip():
            raise ValueError("Task name cannot be empty")
        return value

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

class Tasks(Base):
    __tablename__ = "tasks"
    __table_args__ = (UniqueConstraint('task_name', name='uq_task_name'),)

    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, unique=True)
    status = Column(String)
    associated_user_id = Column(Integer, ForeignKey("users.id"))
