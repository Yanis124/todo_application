from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models import TaskPriority, TaskStatus


# ---- User Schemas ----
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


class LoginRequest(BaseModel):
    email: str
    password: str


# ---- Task Schemas ----
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = ""
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    owner_id: int


# ---- Dashboard Schemas ----
class DashboardStats(BaseModel):
    total_tasks: int
    todo_count: int
    in_progress_count: int
    done_count: int
    overdue_count: int
    high_priority_count: int
