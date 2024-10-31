from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

import auth
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from auth import get_current_user

app = FastAPI()
app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/api", status_code=status.HTTP_200_OK)
async def user(usr: user_dependency, db: db_dependency):
    if usr is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return {"User": usr}

@app.get("/api/tasks")
async def get_tasks(db: db_dependency):
    result = db.query(models.ToDoList).all()
    return result

@app.get("/api/tasks/{task_id}")
async def get_task(task_id: int, db: db_dependency):
    result = db.query(models.ToDoList).filter(models.ToDoList.id == task_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result

@app.post("/api/task")
async def create_task(task: models.Task, db: db_dependency):
    data = models.ToDoList(task_name=task.task_name, status=task.status)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

@app.delete("/api/task/{task_id}")
async def delete_task(task_id: int, db: db_dependency):
    data = db.query(models.ToDoList).filter(models.ToDoList.id == task_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(data)
    db.commit()
    return data

@app.put("/api/task/{task_id}")
async def update_task(task_id: int, task: models.Task, db: db_dependency):
    existing_task = db.query(models.ToDoList).filter(models.ToDoList.id == task_id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    existing_task.task_name = task.task_name
    existing_task.status = task.status

    db.commit()
    db.refresh(existing_task)

    return existing_task
