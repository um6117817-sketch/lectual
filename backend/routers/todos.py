from fastapi import APIRouter, HTTPException, Query, Depends
from database import get_connection
from crud import get_todos, get_todo_by_id, create_todo, update_todo, delete_todo
from schemas import TodoCreate, TodoUpdate, TodoResponse, PaginatedResponse

router = APIRouter(prefix="/todos", tags=["todos"])


def get_db():
    """Dependency that provides a database connection."""
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


@router.get("", response_model=PaginatedResponse[TodoResponse])
def list_todos(
    status: str | None = Query(None, description="Filter by status: todo, in_progress, done"),
    priority: str | None = Query(None, description="Filter by priority: low, medium, high"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    size: int = Query(20, ge=1, le=100, description="Items per page (1-100)"),
    db=Depends(get_db),
):
    """Get a paginated list of todos with optional filtering."""
    items, total = get_todos(db, status=status, priority=priority, page=page, size=size)
    pages = (total + size - 1) // size if total > 0 else 0
    return PaginatedResponse(
        items=[TodoResponse(**item) for item in items],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db=Depends(get_db)):
    """Get a single todo by ID."""
    todo = get_todo_by_id(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    return TodoResponse(**todo)


@router.post("", response_model=TodoResponse, status_code=201)
def create_todo_endpoint(todo: TodoCreate, db=Depends(get_db)):
    """Create a new todo item."""
    result = create_todo(db, todo)
    return TodoResponse(**result)


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo_endpoint(todo_id: int, todo: TodoUpdate, db=Depends(get_db)):
    """Update an existing todo. Only provided fields are updated."""
    result = update_todo(db, todo_id, todo)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    return TodoResponse(**result)


@router.delete("/{todo_id}")
def delete_todo_endpoint(todo_id: int, db=Depends(get_db)):
    """Delete a todo by ID."""
    success = delete_todo(db, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    return {"message": "deleted"}
