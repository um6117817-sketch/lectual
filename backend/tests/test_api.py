import sys
import os

# Use test-specific database path BEFORE importing database module
os.environ["TODO_DB_PATH"] = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_todo.db")

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app
from database import init_db, DB_PATH

# Remove test db if exists
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

client = TestClient(app)


def setup_function():
    """Re-initialize the test database before each test."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()


def test_health_check():
    """TC-01: Health check returns ok."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}


def test_create_todo_valid():
    """TC-02: Create todo with valid data returns 201."""
    response = client.post(
        "/api/v1/todos",
        json={"title": "Test Todo", "description": "A test", "priority": "high"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Todo"
    assert data["description"] == "A test"
    assert data["priority"] == "high"
    assert data["status"] == "todo"
    assert "created_at" in data
    assert "updated_at" in data


def test_create_todo_missing_title():
    """TC-03: Create todo without title returns 422."""
    response = client.post("/api/v1/todos", json={"priority": "low"})
    assert response.status_code == 422


def test_create_todo_empty_title():
    """TC-04: Create todo with empty title returns 422."""
    response = client.post("/api/v1/todos", json={"title": ""})
    assert response.status_code == 422


def test_create_todo_invalid_priority():
    """TC-05: Create todo with invalid priority returns 422."""
    response = client.post("/api/v1/todos", json={"title": "Test", "priority": "urgent"})
    assert response.status_code == 422


def test_get_todos_empty():
    """TC-06: Get todos when empty returns empty list."""
    response = client.get("/api/v1/todos")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["size"] == 20
    assert data["pages"] == 0


def test_get_todos_with_data():
    """TC-07: Get todos with data returns items."""
    client.post("/api/v1/todos", json={"title": "Todo 1"})
    client.post("/api/v1/todos", json={"title": "Todo 2"})
    response = client.get("/api/v1/todos")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_get_todos_filter_by_status():
    """TC-08: Filter todos by status."""
    client.post("/api/v1/todos", json={"title": "Todo A", "status": "todo"})
    client.post("/api/v1/todos", json={"title": "Todo B", "status": "done"})
    response = client.get("/api/v1/todos?status=done")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["status"] == "done"


def test_get_todos_pagination():
    """TC-09: Pagination works correctly."""
    for i in range(5):
        client.post("/api/v1/todos", json={"title": f"Todo {i}"})
    response = client.get("/api/v1/todos?page=1&size=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5
    assert data["page"] == 1
    assert data["size"] == 2
    assert data["pages"] == 3


def test_get_todo_by_id_exists():
    """TC-10: Get single todo that exists."""
    client.post("/api/v1/todos", json={"title": "Single"})
    response = client.get("/api/v1/todos/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Single"


def test_get_todo_by_id_not_found():
    """TC-11: Get single todo that doesn't exist returns 404."""
    response = client.get("/api/v1/todos/999")
    assert response.status_code == 404


def test_update_todo_partial():
    """TC-12: Partial update only changes specified fields."""
    client.post("/api/v1/todos", json={"title": "Original", "priority": "low"})
    response = client.put("/api/v1/todos/1", json={"title": "Updated"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["priority"] == "low"  # unchanged


def test_update_todo_not_found():
    """TC-13: Update non-existent todo returns 404."""
    response = client.put("/api/v1/todos/999", json={"title": "Nope"})
    assert response.status_code == 404


def test_delete_todo_exists():
    """TC-14: Delete existing todo succeeds."""
    client.post("/api/v1/todos", json={"title": "To Delete"})
    response = client.delete("/api/v1/todos/1")
    assert response.status_code == 200
    assert response.json() == {"message": "deleted"}
    # Verify it's gone
    response = client.get("/api/v1/todos/1")
    assert response.status_code == 404


def test_delete_todo_not_found():
    """TC-15: Delete non-existent todo returns 404."""
    response = client.delete("/api/v1/todos/999")
    assert response.status_code == 404


if __name__ == "__main__":
    # Run all tests
    import pytest
    pytest.main([__file__, "-v"])
