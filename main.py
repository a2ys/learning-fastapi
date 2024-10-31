from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

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
