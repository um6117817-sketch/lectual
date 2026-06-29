import sqlite3
import os

DB_PATH = os.environ.get("TODO_DB_PATH", os.path.join(os.path.dirname(__file__), "todo.db"))


def get_connection() -> sqlite3.Connection:
    """Get a new SQLite connection with row_factory set to Row."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL CHECK(length(title) >= 1 AND length(title) <= 200),
            description TEXT DEFAULT '' CHECK(length(description) <= 2000),
            priority TEXT NOT NULL DEFAULT 'medium' CHECK(priority IN ('low', 'medium', 'high')),
            status TEXT NOT NULL DEFAULT 'todo' CHECK(status IN ('todo', 'in_progress', 'done')),
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)

    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS update_todo_timestamp
            AFTER UPDATE ON todos
            FOR EACH ROW
        BEGIN
            UPDATE todos SET updated_at = datetime('now') WHERE id = OLD.id;
        END;
    """)

    conn.commit()
    conn.close()
