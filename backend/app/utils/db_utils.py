"""
Database orchestration utilities.

This module provides higher-level functions that perform SQL operations (via
`sql_utils`) and keep the Chroma vector index in sync (via `app.db.chromadb`).

Use these functions from your route handlers so both stores stay consistent.
"""
from typing import List, Dict, Any, Optional

from app.utils import sql_utils
from app.db.chromadb import (
    get_chroma_connection,
    create_tasks_collection,
    create_notes_collection,
    upsert_task,
    upsert_note,
    delete_task as chroma_delete_task,
    delete_note as chroma_delete_note,
    add_relation as chroma_add_relation,
    remove_relation as chroma_remove_relation,
)


def _get_cols():
    client = get_chroma_connection()
    return create_tasks_collection(client), create_notes_collection(client)


def create_task(title: str, description: str = "", status: str = "pending", deadline: Optional[str] = None) -> int:
    task_id = sql_utils.create_task(title, description, status, deadline)
    # Fetch full task (including notes) and upsert into Chroma
    task = sql_utils.get_task_by_id(task_id)
    tasks_col, notes_col = _get_cols()
    related_notes = [str(n.get('id')) for n in task.get('notes', [])]
    upsert_task(tasks_col, task_id, title, description, status, deadline, related_notes=related_notes)
    return task_id


def update_task(task_id: int, title: str, description: str = "", status: str = "pending", deadline: Optional[str] = None) -> None:
    sql_utils.update_task(task_id, title, description, status, deadline)
    task = sql_utils.get_task_by_id(task_id)
    tasks_col, notes_col = _get_cols()
    related_notes = [str(n.get('id')) for n in task.get('notes', [])]
    upsert_task(tasks_col, task_id, title, description, status, deadline, related_notes=related_notes)


def delete_task(task_id: int) -> None:
    sql_utils.delete_task(task_id)
    tasks_col, notes_col = _get_cols()
    chroma_delete_task(tasks_col, task_id)


def create_note(title: str, content: str = "", created_at: Optional[str] = None) -> int:
    note_id = sql_utils.create_note(title, content, created_at)
    note = sql_utils.get_note_by_id(note_id)
    tasks_col, notes_col = _get_cols()
    related_tasks = [str(t.get('id')) for t in note.get('tasks', [])]
    upsert_note(notes_col, note_id, title, content, created_at, related_tasks=related_tasks)
    return note_id


def update_note(note_id: int, title: str, content: str = "") -> None:
    sql_utils.update_note(note_id, title, content)
    note = sql_utils.get_note_by_id(note_id)
    tasks_col, notes_col = _get_cols()
    related_tasks = [str(t.get('id')) for t in note.get('tasks', [])]
    upsert_note(notes_col, note_id, title, content, note.get('created_at'), related_tasks=related_tasks)


def delete_note(note_id: int) -> None:
    sql_utils.delete_note(note_id)
    tasks_col, notes_col = _get_cols()
    chroma_delete_note(notes_col, note_id)


def add_note_to_task(task_id: int, note_id: int) -> None:
    sql_utils.add_note_to_task(task_id, note_id)
    tasks_col, notes_col = _get_cols()
    chroma_add_relation(tasks_col, notes_col, task_id, note_id, 'related_notes', 'related_tasks')


def remove_note_from_task(task_id: int, note_id: int) -> None:
    sql_utils.remove_note_from_task(task_id, note_id)
    tasks_col, notes_col = _get_cols()
    chroma_remove_relation(tasks_col, notes_col, task_id, note_id, 'related_notes', 'related_tasks')


# Convenience pass-throughs to SQL read functions
def get_all_tasks() -> List[Dict[str, Any]]:
    return sql_utils.get_all_tasks()


def get_all_notes() -> List[Dict[str, Any]]:
    return sql_utils.get_all_notes()


def get_task_by_id(task_id: int) -> Dict[str, Any]:
    return sql_utils.get_task_by_id(task_id)


def get_note_by_id(note_id: int) -> Dict[str, Any]:
    return sql_utils.get_note_by_id(note_id)
