"""Agent-ready Chromadb tools.

This module exposes functions that an agent (e.g., LangChain agent) can call:
- CRUD wrappers -> use `db_utils` so SQL + Chroma stay synced
- Semantic search helpers -> use `chroma_utils` for vector queries

Keep these functions simple and idempotent so agents can call them safely.
"""
from typing import List, Dict, Any, Optional

from app.utils import db_utils
from app.utils import chroma_utils


# --- CRUD wrappers (call db_utils which orchestrates SQL + Chroma) ---
def create_task(title: str, description: str = "", status: str = "pending", deadline: Optional[str] = None) -> int:
    """Create a new task with a title, optional description, status, and deadline.
    
    Args:
        title: The task title (required)
        description: Detailed description of the task (optional)
        status: Task status - use 'pending', 'in_progress', or 'completed' (default: 'pending')
        deadline: Due date in YYYY-MM-DD format (optional)
    
    Returns:
        The ID of the newly created task
    """
    return db_utils.create_task(title, description, status, deadline)


def update_task(task_id: int, title: str, description: str = "", status: str = "pending", deadline: Optional[str] = None) -> None:
    """Update an existing task's details.
    
    Args:
        task_id: The ID of the task to update (required)
        title: New title for the task (required)
        description: Updated description (optional)
        status: Updated status - use 'pending', 'in_progress', or 'completed' (optional)
        deadline: Updated deadline in YYYY-MM-DD format (optional)
    """
    return db_utils.update_task(task_id, title, description, status, deadline)


def delete_task(task_id: int) -> None:
    """Delete a task permanently by its ID.
    
    Args:
        task_id: The ID of the task to delete
    """
    return db_utils.delete_task(task_id)


def create_note(title: str, content: str = "", created_at: Optional[str] = None) -> int:
    """Create a new note with a title and optional content.
    
    Args:
        title: The note title (required)
        content: The note content/body text (optional)
        created_at: Creation timestamp (optional, defaults to now)
    
    Returns:
        The ID of the newly created note
    """
    return db_utils.create_note(title, content, created_at)


def update_note(note_id: int, title: str, content: str = "") -> None:
    """Update an existing note's title and content.
    
    Args:
        note_id: The ID of the note to update (required)
        title: New title for the note (required)
        content: Updated content/body text (optional)
    """
    return db_utils.update_note(note_id, title, content)


def delete_note(note_id: int) -> None:
    """Delete a note permanently by its ID.
    
    Args:
        note_id: The ID of the note to delete
    """
    return db_utils.delete_note(note_id)


def add_note_to_task(task_id: int, note_id: int) -> None:
    """Link/attach a note to a task to show their relationship.
    
    Args:
        task_id: The ID of the task
        note_id: The ID of the note to attach to the task
    """
    return db_utils.add_note_to_task(task_id, note_id)


def remove_note_from_task(task_id: int, note_id: int) -> None:
    """Unlink/detach a note from a task.
    
    Args:
        task_id: The ID of the task
        note_id: The ID of the note to remove from the task
    """
    return db_utils.remove_note_from_task(task_id, note_id)


# --- Vector search / retrieval helpers (call chroma_utils) ---
def search_notes(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Search for notes using semantic similarity (finds notes by meaning, not exact keywords).
    Use this to find notes related to a topic, concept, or question.
    
    Args:
        query: A natural language search query (e.g., "Python programming tips")
        top_k: Maximum number of results to return (default: 5)
    
    Returns:
        List of matching notes with their content and metadata
    """
    return chroma_utils.search_notes(query, top_k=top_k)


def search_tasks(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Search for tasks using semantic similarity (finds tasks by meaning, not exact keywords).
    Use this to find tasks related to a topic, project, or question.
    
    Args:
        query: A natural language search query (e.g., "shopping tasks")
        top_k: Maximum number of results to return (default: 5)
    
    Returns:
        List of matching tasks with their details and metadata
    """
    return chroma_utils.search_tasks(query, top_k=top_k)


def get_note_chroma(note_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a specific note by its ID from the vector database.
    
    Args:
        note_id: The ID of the note to retrieve
    
    Returns:
        The note data or None if not found
    """
    return chroma_utils.get_note_from_chroma(note_id)


def get_task_chroma(task_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a specific task by its ID from the vector database.
    
    Args:
        task_id: The ID of the task to retrieve
    
    Returns:
        The task data or None if not found
    """
    return chroma_utils.get_task_from_chroma(task_id)


# Small RAG helper: Retrieval-Augmented Generation.
def rag_context_for_query(query: str, top_k: int = 5) -> Dict[str, Any]:
    """Get relevant context (both notes and tasks) for answering a question or providing insights.
    Use this when you need to gather information before responding to a complex query.
    
    Args:
        query: A natural language question or topic (e.g., "What are my urgent tasks?")
        top_k: Maximum number of items to retrieve per type (default: 5)
    
    Returns:
        Dictionary with combined context from notes and tasks relevant to the query
    """
    notes = search_notes(query, top_k=top_k)
    tasks = search_tasks(query, top_k=top_k)

    # flatten texts
    context_items = []
    for n in notes:
        context_items.append({"source": "note", "id": n.get("id"), "text": n.get("document"), "meta": n.get("metadata")})
    for t in tasks:
        context_items.append({"source": "task", "id": t.get("id"), "text": t.get("document"), "meta": t.get("metadata")})

    return {"query": query, "items": context_items}
