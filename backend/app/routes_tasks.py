from flask import Blueprint, request, jsonify
from app.db.chroma_manager import get_chroma_manager

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/", methods=["POST"])
def create_task():
    data = request.json
    manager = get_chroma_manager()
    task_id = manager.create_task(
        data["title"],
        data.get("description", ""),
        data.get("status", "pending"),
        data.get("deadline", None)
    )
    return jsonify({"message": "Task created", "id": task_id}), 201


@tasks_bp.route("/", methods=["GET"])
def get_tasks():
    manager = get_chroma_manager()
    tasks = manager.get_all_tasks()
    return jsonify(tasks)


@tasks_bp.route("/<int:id>", methods=["GET"])
def get_task(id):
    manager = get_chroma_manager()
    task = manager.get_task(id)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404


@tasks_bp.route("/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.json
    manager = get_chroma_manager()
    manager.update_task(
        id,
        data.get("title"),
        data.get("description"),
        data.get("status"),
        data.get("deadline")
    )
    return jsonify({"message": "Task updated"})


@tasks_bp.route("/<int:id>", methods=["DELETE"])
def delete_task(id):
    manager = get_chroma_manager()
    manager.delete_task(id)
    return jsonify({"message": "Task deleted"})


@tasks_bp.route("/<int:task_id>/notes/<int:note_id>", methods=["POST"])
def add_note_to_task(task_id, note_id):
    manager = get_chroma_manager()
    manager.add_note_to_task(task_id, note_id)
    return jsonify({"message": "Note added to task"})


@tasks_bp.route("/<int:task_id>/notes/<int:note_id>", methods=["DELETE"])
def remove_note_from_task(task_id, note_id):
    manager = get_chroma_manager()
    manager.remove_note_from_task(task_id, note_id)
    return jsonify({"message": "Note removed from task"})
