from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar, List
from models import PriorityEnum, StatusEnum


class TodoCreate(BaseModel):
    """Schema for creating a new Todo item."""
    title: str = Field(..., min_length=1, max_length=200, description="Title of the todo item")
    description: str = Field(default="", max_length=2000, description="Optional description")
    priority: PriorityEnum = Field(default="medium", description="Priority: low, medium, or high")
    status: StatusEnum = Field(default="todo", description="Status: todo, in_progress, or done")


class TodoUpdate(BaseModel):
    """Schema for updating an existing Todo item. All fields are optional."""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Title of the todo item")
    description: Optional[str] = Field(None, max_length=2000, description="Optional description")
    priority: Optional[PriorityEnum] = Field(None, description="Priority: low, medium, or high")
    status: Optional[StatusEnum] = Field(None, description="Status: todo, in_progress, or done")


class TodoResponse(BaseModel):
    """Schema for a Todo item in API responses."""
    id: int
    title: str
    description: str
    priority: str
    status: str
    created_at: str
    updated_at: str


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
