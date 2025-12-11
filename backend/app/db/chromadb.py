import chromadb
import json

PERSIST_DIR = "./chroma_persist"


def get_chroma_connection():
    """Return a new ChromaDB persistent client."""
    # Using PersistentClient to keep data on disk between runs
    try:
        client = chromadb.PersistentClient(path=PERSIST_DIR)
    except Exception:
        # fallback to default Client if PersistentClient isn't available
        client = chromadb.Client()
    return client


def create_tasks_collection(client):
    """Get or create the 'tasks' collection."""
    try:
        return client.get_collection(name="tasks")
    except Exception:
        return client.create_collection(name="tasks")


def create_notes_collection(client):
    """Get or create the 'notes' collection."""
    try:
        return client.get_collection(name="notes")
    except Exception:
        return client.create_collection(name="notes")


def _task_document_text(title, description, status, deadline):
    return f"{title or ''}\n\n{description or ''}\n\nStatus: {status or ''}\nDeadline: {deadline or ''}"


def _note_document_text(title, content):
    return f"{title or ''}\n\n{content or ''}"


def upsert_task(collection, task_id, title, description, status, deadline, related_notes=None):
    """Create or update a task document in Chroma with metadata (including relations)."""
    doc = _task_document_text(title, description, status, deadline)
    # Store relation lists as JSON strings because Chroma metadata values must be primitive types
    metadata = {
        "task_id": str(task_id),
        "title": title,
        "status": status,
        "deadline": deadline,
        "related_notes": json.dumps([str(n) for n in (related_notes or [])])
    }
    # Use upsert so existing id is replaced
    collection.upsert(ids=[str(task_id)], documents=[doc], metadatas=[metadata])
    # persist if client supports it
    try:
        collection._client.persist()
    except Exception:
        pass


def upsert_note(collection, note_id, title, content, created_at=None, related_tasks=None):
    """Create or update a note document in Chroma with metadata (including relations)."""
    doc = _note_document_text(title, content)
    metadata = {
        "note_id": str(note_id),
        "title": title,
        "created_at": created_at,
        "related_tasks": json.dumps([str(t) for t in (related_tasks or [])])
    }
    collection.upsert(ids=[str(note_id)], documents=[doc], metadatas=[metadata])
    try:
        collection._client.persist()
    except Exception:
        pass


def delete_task(collection, task_id):
    try:
        collection.delete(ids=[str(task_id)])
    except Exception:
        pass
    try:
        collection._client.persist()
    except Exception:
        pass


def delete_note(collection, note_id):
    try:
        collection.delete(ids=[str(note_id)])
    except Exception:
        pass
    try:
        collection._client.persist()
    except Exception:
        pass


def add_relation(collection_from, collection_to, from_id, to_id, from_field, to_field):
    """Update metadata arrays on both documents to reflect a relation.
    `from_field` and `to_field` are metadata keys like 'related_notes' or 'related_tasks'.
    Relations are stored as JSON strings in metadata to satisfy Chroma's primitive-type requirement.
    """
    # fetch current metadata for from_id
    try:
        res_from = collection_from.get(ids=[str(from_id)])
        meta_from = res_from["metadatas"][0]
    except Exception:
        meta_from = {}

    try:
        res_to = collection_to.get(ids=[str(to_id)])
        meta_to = res_to["metadatas"][0]
    except Exception:
        meta_to = {}

    def _parse_list(value):
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return parsed
            except Exception:
                pass
        return []

    list_from = set(_parse_list(meta_from.get(from_field, [])))
    list_to = set(_parse_list(meta_to.get(to_field, [])))

    list_from.add(str(to_id))
    list_to.add(str(from_id))

    meta_from[from_field] = json.dumps(list(list_from))
    meta_to[to_field] = json.dumps(list(list_to))

    # re-upsert documents with updated metadata
    try:
        doc_from = collection_from.get(ids=[str(from_id)])["documents"][0]
    except Exception:
        doc_from = None
    try:
        doc_to = collection_to.get(ids=[str(to_id)])["documents"][0]
    except Exception:
        doc_to = None

    if doc_from:
        collection_from.upsert(ids=[str(from_id)], documents=[doc_from], metadatas=[meta_from])
    if doc_to:
        collection_to.upsert(ids=[str(to_id)], documents=[doc_to], metadatas=[meta_to])

    try:
        collection_from._client.persist()
    except Exception:
        pass


def remove_relation(collection_from, collection_to, from_id, to_id, from_field, to_field):
    try:
        res_from = collection_from.get(ids=[str(from_id)])
        meta_from = res_from["metadatas"][0]
    except Exception:
        meta_from = {}

    try:
        res_to = collection_to.get(ids=[str(to_id)])
        meta_to = res_to["metadatas"][0]
    except Exception:
        meta_to = {}

    def _parse_list(value):
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return parsed
            except Exception:
                pass
        return []

    list_from = set(_parse_list(meta_from.get(from_field, [])))
    list_to = set(_parse_list(meta_to.get(to_field, [])))

    list_from.discard(str(to_id))
    list_to.discard(str(from_id))

    meta_from[from_field] = json.dumps(list(list_from))
    meta_to[to_field] = json.dumps(list(list_to))

    try:
        doc_from = collection_from.get(ids=[str(from_id)])["documents"][0]
    except Exception:
        doc_from = None
    try:
        doc_to = collection_to.get(ids=[str(to_id)])["documents"][0]
    except Exception:
        doc_to = None

    if doc_from:
        collection_from.upsert(ids=[str(from_id)], documents=[doc_from], metadatas=[meta_from])
    if doc_to:
        collection_to.upsert(ids=[str(to_id)], documents=[doc_to], metadatas=[meta_to])

    try:
        collection_from._client.persist()
    except Exception:
        pass