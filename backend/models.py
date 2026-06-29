from pydantic import BaseModel
from typing import Literal

PriorityEnum = Literal["low", "medium", "high"]
StatusEnum = Literal["todo", "in_progress", "done"]


class TodoItem(BaseModel):
    """Complete Todo item as stored in the database."""
    id: int
    title: str
    description: str = ""
    priority: PriorityEnum = "medium"
    status: StatusEnum = "todo"
    created_at: str
    updated_at: str
