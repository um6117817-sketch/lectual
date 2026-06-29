import sqlite3
from typing import Tuple, Optional, List, Dict, Any
from schemas import TodoCreate, TodoUpdate


def _row_to_dict(row: sqlite3.Row) -> dict:
    """Convert a sqlite3.Row to a plain dict."""
    return dict(row)


def get_todos(
    db: sqlite3.Connection,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    page: int = 1,
    size: int = 20,
) -> Tuple[List[dict], int]:
    """Get a paginated list of todos with optional filtering."""
    cursor = db.cursor()

    conditions = []
    params: list = []

    if status:
        conditions.append("status = ?")
        params.append(status)

    if priority:
        conditions.append("priority = ?")
        params.append(priority)

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    # Get total count
    count_sql = f"SELECT COUNT(*) FROM todos {where_clause}"
    cursor.execute(count_sql, params)
    total = cursor.fetchone()[0]

    # Get paginated items
    offset = (page - 1) * size
    query_sql = f"SELECT * FROM todos {where_clause} ORDER BY created_at DESC LIMIT ? OFFSET ?"
    cursor.execute(query_sql, params + [size, offset])
    items = [_row_to_dict(row) for row in cursor.fetchall()]

    return items, total


def get_todo_by_id(db: sqlite3.Connection, todo_id: int) -> Optional[dict]:
    """Get a single todo by ID. Returns None if not found."""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    if row is None:
        return None
    return _row_to_dict(row)


def create_todo(db: sqlite3.Connection, todo: TodoCreate) -> dict:
    """Create a new todo and return the complete record."""
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO todos (title, description, priority, status) VALUES (?, ?, ?, ?)",
        (todo.title, todo.description, todo.priority, todo.status),
    )
    db.commit()
    todo_id = cursor.lastrowid
    return get_todo_by_id(db, todo_id)


def update_todo(db: sqlite3.Connection, todo_id: int, todo: TodoUpdate) -> Optional[dict]:
    """Update an existing todo. Only updates fields that were explicitly set.
    Returns the updated record or None if not found."""
    cursor = db.cursor()

    # Check if todo exists
    existing = get_todo_by_id(db, todo_id)
    if existing is None:
        return None

    # Get only the fields that were explicitly set
    update_data = todo.model_dump(exclude_unset=True)

    if not update_data:
        # Nothing to update
        return existing

    set_clauses = []
    params = []

    for field, value in update_data.items():
        set_clauses.append(f"{field} = ?")
        params.append(value)

    params.append(todo_id)
    sql = f"UPDATE todos SET {', '.join(set_clauses)} WHERE id = ?"
    cursor.execute(sql, params)
    db.commit()

    return get_todo_by_id(db, todo_id)


def delete_todo(db: sqlite3.Connection, todo_id: int) -> bool:
    """Delete a todo by ID. Returns True if deleted, False if not found."""
    cursor = db.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    db.commit()
    return cursor.rowcount > 0
