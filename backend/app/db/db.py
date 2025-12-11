import sqlite3
import chromadb
from chromadb.config import Settings

DB_NAME = "vault.db"


def init_db():
    """Create the SQLite database file and required tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT,
            deadline TEXT
        )
    """)

    # Notes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            created_at TEXT
        )
    """)

    # Task-Notes junction table (many-to-many)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_notes (
            task_id INTEGER NOT NULL,
            note_id INTEGER NOT NULL,
            PRIMARY KEY (task_id, note_id),
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
            FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
 

def get_db_connection():
    """Return a new SQLite connection to the persistent `vault.db` file."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

