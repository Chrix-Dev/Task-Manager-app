
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from database import supabase
import uuid

router = APIRouter()

# Pydantic models
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    owner_id: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Task(TaskBase):
    id: str
    completed: bool

# Create a task
@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    task_id = str(uuid.uuid4())
    data = task.dict()
    data.update({"id": task_id, "completed": False})
    response = supabase.table("Tasks").insert(data).execute()
    if hasattr(response, 'error') and response.error:
        raise HTTPException(status_code=400, detail=str(response.error))
    return Task(id=task_id, completed=False, **task.dict())

# Get all tasks (optionally filter by owner_id)
@router.get("/tasks", response_model=List[Task])
def get_tasks(owner_id: Optional[str] = None):
    query = supabase.table("Tasks")
    if owner_id:
        query = query.select("*").eq("owner_id", owner_id)
    else:
        query = query.select("*")
    response = query.execute()
    if hasattr(response, 'error') and response.error:
        raise HTTPException(status_code=400, detail=str(response.error))
    return response.data

# Get a single task by ID
@router.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    response = supabase.table("Tasks").select("*").eq("id", task_id).single().execute()
    if hasattr(response, 'error') and response.error:
        raise HTTPException(status_code=404, detail="Task not found")
    return response.data


# Update a task (with clear logic and comments)
@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task: TaskUpdate):
    # Prepare the fields to update (ignore None values)
    update_data = {}
    if task.title is not None:
        update_data["title"] = task.title
    if task.completed is not None:
        update_data["completed"] = task.completed

    # If no fields provided, return an error
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update.")

    # Update the task in the database
    response = supabase.table("Tasks").update(update_data).eq("id", task_id).execute()
    if hasattr(response, 'error') and response.error:
        raise HTTPException(status_code=400, detail=str(response.error))

    # Fetch and return the updated task
    updated = supabase.table("Tasks").select("*").eq("id", task_id).single().execute()
    if hasattr(updated, 'error') and updated.error:
        raise HTTPException(status_code=404, detail="Task not found after update.")
    return updated.data

# Delete a task
@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    response = supabase.table("Tasks").delete().eq("id", task_id).execute()
    if hasattr(response, 'error') and response.error:
        raise HTTPException(status_code=400, detail=str(response.error))
    return None


