from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    title: str
    status: Optional[str] = "pending"  # Valores: pending, in_progress, done

class TaskCreate(TaskBase):
    project_id: int

class TaskResponse(TaskBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True

class TaskUpdateStatus(BaseModel):
    status: str  # pending, in_progress, done