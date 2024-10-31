from pydantic import BaseModel
from typing import List, Literal
from sqlalchemy import Column, String, Integer
from database import Base


class Task(BaseModel):
    task_name: str
    status: Literal["all", "active", "completed"]


class ToDoList(Base):
    __tablename__ = "todolist"

    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, index=True)
    status = Column(String, index=True)
