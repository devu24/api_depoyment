from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Data model for a task

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# In-memory database
tasks = {}

# POST → Create a new task
@app.post("/tasks/")
def create_task(task: Task):
    task_id = len(tasks) + 1
    tasks[task_id] = task
    return {"id": task_id, "task": task}

# GET → Retrieve all tasks or a specific one
@app.get("/tasks/")
def get_all_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

# PUT → Update an existing task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = task
    return {"id": task_id, "task": task}

# DELETE → Remove a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return {"message": "Task deleted successfully"}


