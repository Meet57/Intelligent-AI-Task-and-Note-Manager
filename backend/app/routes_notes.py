from flask import Blueprint, request, jsonify
from app.db.chroma_manager import get_chroma_manager
import datetime

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/", methods=["POST"])
def create_note():
    data = request.json
    created_at = datetime.datetime.now().isoformat()
    manager = get_chroma_manager()
    
    note_id = manager.create_note(
        data["title"],
        data.get("content", ""),
        created_at
    )
    return jsonify({"message": "Note created", "id": note_id}), 201


@notes_bp.route("/", methods=["GET"])
def get_notes():
    manager = get_chroma_manager()
    notes = manager.get_all_notes()
    return jsonify(notes)


@notes_bp.route("/<int:id>", methods=["GET"])
def get_note(id):
    manager = get_chroma_manager()
    note = manager.get_note(id)
    if note:
        return jsonify(note)
    return jsonify({"error": "Note not found"}), 404


@notes_bp.route("/<int:id>", methods=["PUT", "PATCH"])
def update_note(id):
    data = request.json
    manager = get_chroma_manager()
    manager.update_note(
        id,
        data.get("title"),
        data.get("content")
    )
    return jsonify({"message": "Note updated"})


@notes_bp.route("/<int:id>", methods=["DELETE"])
def delete_note(id):
    manager = get_chroma_manager()
    manager.delete_note(id)
    return jsonify({"message": "Note deleted"})


@notes_bp.route("/<int:note_id>/tasks/<int:task_id>", methods=["POST"])
def add_task_to_note(note_id, task_id):
    manager = get_chroma_manager()
    manager.add_note_to_task(task_id, note_id)
    return jsonify({"message": "Task added to note"})


@notes_bp.route("/<int:note_id>/tasks/<int:task_id>", methods=["DELETE"])
def remove_task_from_note(note_id, task_id):
    manager = get_chroma_manager()
    manager.remove_note_from_task(task_id, note_id)
    return jsonify({"message": "Task removed from note"})
