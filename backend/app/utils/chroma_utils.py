from app.db.chromadb import upsert_task, upsert_note, create_tasks_collection, create_notes_collection, get_chroma_connection
from app.utils.db_utils import get_all_tasks, get_all_notes

def fetch_tasks_and_load_to_chromadb():
    """Fetch all tasks from the SQL database and load them into ChromaDB."""
    client = get_chroma_connection()
    tasks_collection = create_tasks_collection(client)
    tasks = get_all_tasks()

    for task in tasks:
        related_notes = [str(n.get('id')) for n in task.get('notes', [])]
        upsert_task(
            tasks_collection,
            task_id=task.get('id'),
            title=task.get('title'),
            description=task.get('description'),
            status=task.get('status'),
            deadline=task.get('deadline'),
            related_notes=related_notes,
        )

def fetch_notes_and_load_to_chromadb():
    """Fetch all notes from the SQL database and load them into ChromaDB."""
    client = get_chroma_connection()
    notes_collection = create_notes_collection(client)
    notes = get_all_notes()

    for note in notes:
        related_tasks = [str(t.get('id')) for t in note.get('tasks', [])]
        upsert_note(
            notes_collection,
            note_id=note.get('id'),
            title=note.get('title'),
            content=note.get('content'),
            created_at=note.get('created_at'),
            related_tasks=related_tasks,
        )


def _parse_metadata(meta: dict) -> dict:
    """Parse metadata values (deserialize JSON lists for relations)."""
    if not meta:
        return {}
    parsed = dict(meta)
    # parse relation fields if present
    for key in list(parsed.keys()):
        if key.startswith("related_") and isinstance(parsed[key], str):
            try:
                parsed[key] = __import__("json").loads(parsed[key])
            except Exception:
                # leave as string if parsing fails
                pass
    return parsed


def search_notes(query: str, top_k: int = 5):
    """Semantic search notes collection using query text.

    Returns a list of results with fields: id, document, metadata (parsed).
    """
    client = get_chroma_connection()
    notes_col = create_notes_collection(client)
    try:
        res = notes_col.query(query_texts=[query], n_results=top_k, include=["documents", "metadatas"])
    except TypeError:
        # fallback for older chroma versions
        res = notes_col.query(query_texts=[query], top_k=top_k, include=["documents", "metadatas"])

    results = []
    ids = res.get("ids", [[]])[0]
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    for i in range(len(ids)):
        results.append({
            "id": ids[i],
            "document": docs[i],
            "metadata": _parse_metadata(metas[i])
        })
    return results


def search_tasks(query: str, top_k: int = 5):
    """Semantic search tasks collection using query text.

    Returns a list of results with fields: id, document, metadata (parsed).
    """
    client = get_chroma_connection()
    tasks_col = create_tasks_collection(client)
    try:
        res = tasks_col.query(query_texts=[query], n_results=top_k, include=["documents", "metadatas"])
    except TypeError:
        res = tasks_col.query(query_texts=[query], top_k=top_k, include=["documents", "metadatas"])

    results = []
    ids = res.get("ids", [[]])[0]
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    for i in range(len(ids)):
        results.append({
            "id": ids[i],
            "document": docs[i],
            "metadata": _parse_metadata(metas[i])
        })
    return results


def get_note_from_chroma(note_id: int):
    """Retrieve a single note document & metadata from Chroma by id."""
    client = get_chroma_connection()
    notes_col = create_notes_collection(client)
    try:
        res = notes_col.get(ids=[str(note_id)], include=["documents", "metadatas"])
    except Exception:
        return None
    try:
        return {
            "id": res.get("ids", [[]])[0],
            "document": res.get("documents", [])[0],
            "metadata": _parse_metadata(res.get("metadatas", [])[0])
        }
    except Exception:
        return None


def get_task_from_chroma(task_id: int):
    """Retrieve a single task document & metadata from Chroma by id."""
    client = get_chroma_connection()
    tasks_col = create_tasks_collection(client)
    try:
        res = tasks_col.get(ids=[str(task_id)], include=["documents", "metadatas"])
    except Exception:
        return None
    try:
        return {
            "id": res.get("ids", [])[0],
            "document": res.get("documents", [])[0],
            "metadata": _parse_metadata(res.get("metadatas", [])[0])
        }
    except Exception:
        return None