from app.db.db import get_db_connection

# TASKS CRUD

def create_task(title, description="", status="pending", deadline=None):
    """Create a new task."""
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO tasks (title, description, status, deadline) VALUES (?, ?, ?, ?)",
        (title, description, status, deadline)
    )
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id


def get_all_tasks():
    """Get all tasks with their associated notes."""
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    
    result = []
    for task in tasks:
        task_dict = dict(task)
        task_dict["notes"] = get_task_notes(task["id"])
        result.append(task_dict)
    
    conn.close()
    return result


def get_task_by_id(task_id):
    """Get a single task by ID with its notes."""
    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    
    if not task:
        return None
    
    task_dict = dict(task)
    task_dict["notes"] = get_task_notes(task_id)
    return task_dict


def update_task(task_id, title, description="", status="pending", deadline=None):
    """Update an existing task."""
    conn = get_db_connection()
    conn.execute(
        "UPDATE tasks SET title=?, description=?, status=?, deadline=? WHERE id=?",
        (title, description, status, deadline, task_id)
    )
    conn.commit()
    conn.close()
    


def delete_task(task_id):
    """Delete a task and its note associations."""
    conn = get_db_connection()
    conn.execute("DELETE FROM task_notes WHERE task_id=?", (task_id,))
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    

# NOTES CRUD

def create_note(title, content="", created_at=None):
    """Create a new note."""
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)",
        (title, content, created_at)
    )
    note_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return note_id


def get_all_notes():
    """Get all notes with their associated tasks."""
    conn = get_db_connection()
    notes = conn.execute("SELECT * FROM notes").fetchall()
    
    result = []
    for note in notes:
        note_dict = dict(note)
        note_dict["tasks"] = get_note_tasks(note["id"])
        result.append(note_dict)
    
    conn.close()
    return result


def get_note_by_id(note_id):
    """Get a single note by ID with its tasks."""
    conn = get_db_connection()
    note = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,)).fetchone()
    conn.close()
    
    if not note:
        return None
    
    note_dict = dict(note)
    note_dict["tasks"] = get_note_tasks(note_id)
    return note_dict


def update_note(note_id, title, content=""):
    """Update an existing note."""
    conn = get_db_connection()
    conn.execute(
        "UPDATE notes SET title=?, content=? WHERE id=?",
        (title, content, note_id)
    )
    conn.commit()
    conn.close()
    


def delete_note(note_id):
    """Delete a note and its task associations."""
    conn = get_db_connection()
    conn.execute("DELETE FROM task_notes WHERE note_id=?", (note_id,))
    conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    


# TASK-NOTES RELATIONSHIP (MANY-TO-MANY)

def add_note_to_task(task_id, note_id):
    """Associate a note with a task."""
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT * FROM task_notes WHERE task_id=? AND note_id=?",
        (task_id, note_id)
    ).fetchone()
    
    if not existing:
        conn.execute(
            "INSERT INTO task_notes (task_id, note_id) VALUES (?, ?)",
            (task_id, note_id)
        )
        conn.commit()
    conn.close()
    


def remove_note_from_task(task_id, note_id):
    """Remove a note association from a task."""
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM task_notes WHERE task_id=? AND note_id=?",
        (task_id, note_id)
    )
    conn.commit()
    conn.close()
    


def get_task_notes(task_id):
    """Get all notes for a specific task."""
    conn = get_db_connection()
    notes = conn.execute("""
        SELECT n.* FROM notes n
        INNER JOIN task_notes tn ON n.id = tn.note_id
        WHERE tn.task_id = ?
    """, (task_id,)).fetchall()
    conn.close()
    return [dict(note) for note in notes]


def get_note_tasks(note_id):
    """Get all tasks for a specific note."""
    conn = get_db_connection()
    tasks = conn.execute("""
        SELECT t.* FROM tasks t
        INNER JOIN task_notes tn ON t.id = tn.task_id
        WHERE tn.note_id = ?
    """, (note_id,)).fetchall()
    conn.close()
    return [dict(task) for task in tasks]
