from pydantic import BaseModel
from typing import Literal
from sqlalchemy import Column, String, Integer, ForeignKey
from database import Base


class Task(BaseModel):
    task_name: str
    status: Literal["active", "completed"]

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

class Tasks(Base):
    __tablename__ = "tasks"


    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, unique=True)
    status = Column(String)
    associated_user_id = Column(Integer, ForeignKey("users.id"))
