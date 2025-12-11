"""Simplified ChromaDB manager - Single source of truth for tasks and notes.

This module follows DRY and KISS principles:
- One place for all CRUD operations
- Direct ChromaDB operations (no SQL layer)
- Simple, clear functions
"""
import chromadb
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

PERSIST_DIR = "./chroma_persist"


class ChromaManager:
    """Singleton manager for ChromaDB operations."""
    
    def __init__(self):
        self.client = chromadb.PersistentClient(path=PERSIST_DIR)
        self.tasks_col = self._get_or_create_collection("tasks")
        self.notes_col = self._get_or_create_collection("notes")
        self._id_counter_tasks = self._get_max_id(self.tasks_col)
        self._id_counter_notes = self._get_max_id(self.notes_col)
    
    def _get_or_create_collection(self, name: str):
        """Get or create a collection."""
        try:
            return self.client.get_collection(name=name)
        except Exception:
            return self.client.create_collection(name=name)
    
    def _get_max_id(self, collection) -> int:
        """Get the highest ID in a collection."""
        try:
            result = collection.get()
            if result and result.get("ids"):
                return max([int(id_str) for id_str in result["ids"]])
        except Exception:
            pass
        return 0
    
    def _next_task_id(self) -> int:
        """Generate next task ID."""
        self._id_counter_tasks += 1
        return self._id_counter_tasks
    
    def _next_note_id(self) -> int:
        """Generate next note ID."""
        self._id_counter_notes += 1
        return self._id_counter_notes
    
    # ===== TASK OPERATIONS =====
    
    def create_task(self, title: str, description: str = "", status: str = "pending", 
                   deadline: Optional[str] = None) -> int:
        """Create a new task."""
        task_id = self._next_task_id()
        doc = f"{title}\n\n{description}\n\nStatus: {status}\nDeadline: {deadline or 'None'}"
        metadata = {
            "id": str(task_id),
            "title": title,
            "description": description or "",
            "status": status,
            "deadline": deadline or "",
            "related_notes": "[]"
        }
        self.tasks_col.upsert(ids=[str(task_id)], documents=[doc], metadatas=[metadata])
        return task_id
    
    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get a task by ID."""
        try:
            result = self.tasks_col.get(ids=[str(task_id)], include=["documents", "metadatas"])
            if result["ids"]:
                meta = result["metadatas"][0]
                related_notes = json.loads(meta.get("related_notes", "[]"))
                return {
                    "id": int(result["ids"][0]),
                    "title": meta.get("title", ""),
                    "description": meta.get("description", ""),
                    "status": meta.get("status", "pending"),
                    "deadline": meta.get("deadline", ""),
                    "notes": [self.get_note(int(nid)) for nid in related_notes if self.get_note(int(nid))]
                }
        except Exception as e:
            print(f"Error getting task {task_id}: {e}")
        return None
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks."""
        try:
            result = self.tasks_col.get(include=["metadatas"])
            tasks = []
            for i, task_id in enumerate(result["ids"]):
                meta = result["metadatas"][i]
                related_notes = json.loads(meta.get("related_notes", "[]"))
                tasks.append({
                    "id": int(task_id),
                    "title": meta.get("title", ""),
                    "description": meta.get("description", ""),
                    "status": meta.get("status", "pending"),
                    "deadline": meta.get("deadline", ""),
                    "notes": [self.get_note(int(nid)) for nid in related_notes if self.get_note(int(nid))]
                })
            return sorted(tasks, key=lambda x: x["id"])
        except Exception as e:
            print(f"Error getting all tasks: {e}")
            return []
    
    def update_task(self, task_id: int, title: str, description: str = "", 
                   status: str = "pending", deadline: Optional[str] = None) -> None:
        """Update a task."""
        task = self.get_task(task_id)
        if not task:
            return
        
        doc = f"{title}\n\n{description}\n\nStatus: {status}\nDeadline: {deadline or 'None'}"
        related_notes = [str(n["id"]) for n in task.get("notes", [])]
        metadata = {
            "id": str(task_id),
            "title": title,
            "description": description or "",
            "status": status,
            "deadline": deadline or "",
            "related_notes": json.dumps(related_notes)
        }
        self.tasks_col.upsert(ids=[str(task_id)], documents=[doc], metadatas=[metadata])
    
    def delete_task(self, task_id: int) -> None:
        """Delete a task."""
        try:
            self.tasks_col.delete(ids=[str(task_id)])
        except Exception as e:
            print(f"Error deleting task {task_id}: {e}")
    
    # ===== NOTE OPERATIONS =====
    
    def create_note(self, title: str, content: str = "", created_at: Optional[str] = None) -> int:
        """Create a new note."""
        note_id = self._next_note_id()
        if not created_at:
            created_at = datetime.now().isoformat()
        
        doc = f"{title}\n\n{content}"
        metadata = {
            "id": str(note_id),
            "title": title,
            "content": content or "",
            "created_at": created_at,
            "related_tasks": "[]"
        }
        self.notes_col.upsert(ids=[str(note_id)], documents=[doc], metadatas=[metadata])
        return note_id
    
    def get_note(self, note_id: int) -> Optional[Dict[str, Any]]:
        """Get a note by ID."""
        try:
            result = self.notes_col.get(ids=[str(note_id)], include=["documents", "metadatas"])
            if result["ids"]:
                meta = result["metadatas"][0]
                related_tasks = json.loads(meta.get("related_tasks", "[]"))
                return {
                    "id": int(result["ids"][0]),
                    "title": meta.get("title", ""),
                    "content": meta.get("content", ""),
                    "created_at": meta.get("created_at", ""),
                    "tasks": [{"id": int(tid)} for tid in related_tasks]
                }
        except Exception as e:
            print(f"Error getting note {note_id}: {e}")
        return None
    
    def get_all_notes(self) -> List[Dict[str, Any]]:
        """Get all notes."""
        try:
            result = self.notes_col.get(include=["metadatas"])
            notes = []
            for i, note_id in enumerate(result["ids"]):
                meta = result["metadatas"][i]
                related_tasks = json.loads(meta.get("related_tasks", "[]"))
                notes.append({
                    "id": int(note_id),
                    "title": meta.get("title", ""),
                    "content": meta.get("content", ""),
                    "created_at": meta.get("created_at", ""),
                    "tasks": [{"id": int(tid)} for tid in related_tasks]
                })
            return sorted(notes, key=lambda x: x["id"])
        except Exception as e:
            print(f"Error getting all notes: {e}")
            return []
    
    def update_note(self, note_id: int, title: str, content: str = "") -> None:
        """Update a note."""
        note = self.get_note(note_id)
        if not note:
            return
        
        doc = f"{title}\n\n{content}"
        related_tasks = [str(t["id"]) for t in note.get("tasks", [])]
        metadata = {
            "id": str(note_id),
            "title": title,
            "content": content or "",
            "created_at": note["created_at"],
            "related_tasks": json.dumps(related_tasks)
        }
        self.notes_col.upsert(ids=[str(note_id)], documents=[doc], metadatas=[metadata])
    
    def delete_note(self, note_id: int) -> None:
        """Delete a note."""
        try:
            self.notes_col.delete(ids=[str(note_id)])
        except Exception as e:
            print(f"Error deleting note {note_id}: {e}")
    
    # ===== RELATION OPERATIONS =====
    
    def add_note_to_task(self, task_id: int, note_id: int) -> None:
        """Link a note to a task."""
        task = self.get_task(task_id)
        note = self.get_note(note_id)
        if not task or not note:
            return
        
        # Update task's related_notes
        related_notes = [str(n["id"]) for n in task.get("notes", [])]
        if str(note_id) not in related_notes:
            related_notes.append(str(note_id))
        
        doc = f"{task['title']}\n\n{task['description']}\n\nStatus: {task['status']}\nDeadline: {task['deadline'] or 'None'}"
        metadata = {
            "id": str(task_id),
            "title": task["title"],
            "description": task["description"],
            "status": task["status"],
            "deadline": task["deadline"],
            "related_notes": json.dumps(related_notes)
        }
        self.tasks_col.upsert(ids=[str(task_id)], documents=[doc], metadatas=[metadata])
        
        # Update note's related_tasks
        related_tasks = [str(t["id"]) for t in note.get("tasks", [])]
        if str(task_id) not in related_tasks:
            related_tasks.append(str(task_id))
        
        doc_note = f"{note['title']}\n\n{note['content']}"
        metadata_note = {
            "id": str(note_id),
            "title": note["title"],
            "content": note["content"],
            "created_at": note["created_at"],
            "related_tasks": json.dumps(related_tasks)
        }
        self.notes_col.upsert(ids=[str(note_id)], documents=[doc_note], metadatas=[metadata_note])
    
    def remove_note_from_task(self, task_id: int, note_id: int) -> None:
        """Unlink a note from a task."""
        task = self.get_task(task_id)
        note = self.get_note(note_id)
        if not task or not note:
            return
        
        # Update task's related_notes
        related_notes = [str(n["id"]) for n in task.get("notes", [])]
        if str(note_id) in related_notes:
            related_notes.remove(str(note_id))
        
        doc = f"{task['title']}\n\n{task['description']}\n\nStatus: {task['status']}\nDeadline: {task['deadline'] or 'None'}"
        metadata = {
            "id": str(task_id),
            "title": task["title"],
            "description": task["description"],
            "status": task["status"],
            "deadline": task["deadline"],
            "related_notes": json.dumps(related_notes)
        }
        self.tasks_col.upsert(ids=[str(task_id)], documents=[doc], metadatas=[metadata])
        
        # Update note's related_tasks
        related_tasks = [str(t["id"]) for t in note.get("tasks", [])]
        if str(task_id) in related_tasks:
            related_tasks.remove(str(task_id))
        
        doc_note = f"{note['title']}\n\n{note['content']}"
        metadata_note = {
            "id": str(note_id),
            "title": note["title"],
            "content": note["content"],
            "created_at": note["created_at"],
            "related_tasks": json.dumps(related_tasks)
        }
        self.notes_col.upsert(ids=[str(note_id)], documents=[doc_note], metadatas=[metadata_note])
    
    # ===== SEARCH OPERATIONS =====
    
    def search_tasks(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Semantic search for tasks."""
        try:
            result = self.tasks_col.query(query_texts=[query], n_results=top_k, 
                                         include=["documents", "metadatas"])
            tasks = []
            for i in range(len(result["ids"][0])):
                meta = result["metadatas"][0][i]
                tasks.append({
                    "id": int(result["ids"][0][i]),
                    "document": result["documents"][0][i],
                    "metadata": meta
                })
            return tasks
        except Exception as e:
            print(f"Error searching tasks: {e}")
            return []
    
    def search_notes(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Semantic search for notes."""
        try:
            result = self.notes_col.query(query_texts=[query], n_results=top_k,
                                         include=["documents", "metadatas"])
            notes = []
            for i in range(len(result["ids"][0])):
                meta = result["metadatas"][0][i]
                notes.append({
                    "id": int(result["ids"][0][i]),
                    "document": result["documents"][0][i],
                    "metadata": meta
                })
            return notes
        except Exception as e:
            print(f"Error searching notes: {e}")
            return []


# Global instance
_chroma_manager = None


def get_chroma_manager() -> ChromaManager:
    """Get or create the global ChromaManager instance."""
    global _chroma_manager
    if _chroma_manager is None:
        _chroma_manager = ChromaManager()
    return _chroma_manager
