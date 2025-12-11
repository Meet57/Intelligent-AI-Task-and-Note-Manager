from flask import Blueprint, request, jsonify
from app.utils import db_utils
import datetime

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/", methods=["POST"])
def create_note():
    data = request.json
    created_at = datetime.datetime.now().isoformat()
    
    note_id = db_utils.create_note(
        data["title"],
        data.get("content", ""),
        created_at
    )
    return jsonify({"message": "Note created", "id": note_id}), 201


@notes_bp.route("/", methods=["GET"])
def get_notes():
    notes = db_utils.get_all_notes()
    return jsonify(notes)


@notes_bp.route("/<int:id>", methods=["GET"])
def get_note(id):
    note = db_utils.get_note_by_id(id)
    if note:
        return jsonify(note)
    return jsonify({"error": "Note not found"}), 404


@notes_bp.route("/<int:id>", methods=["PUT"])
def update_note(id):
    data = request.json
    db_utils.update_note(
        id,
        data["title"],
        data.get("content", "")
    )
    return jsonify({"message": "Note updated"})


@notes_bp.route("/<int:id>", methods=["DELETE"])
def delete_note(id):
    db_utils.delete_note(id)
    return jsonify({"message": "Note deleted"})


@notes_bp.route("/<int:note_id>/tasks/<int:task_id>", methods=["POST"])
def add_task_to_note(note_id, task_id):
    db_utils.add_note_to_task(task_id, note_id)
    return jsonify({"message": "Task added to note"})


@notes_bp.route("/<int:note_id>/tasks/<int:task_id>", methods=["DELETE"])
def remove_task_from_note(note_id, task_id):
    db_utils.remove_note_from_task(task_id, note_id)
    return jsonify({"message": "Task removed from note"})