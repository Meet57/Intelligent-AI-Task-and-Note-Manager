from flask import Blueprint, request, jsonify
from app.utils import db_utils

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/", methods=["POST"])
def create_task():
    data = request.json
    task_id = db_utils.create_task(
        data["title"],
        data.get("description", ""),
        data.get("status", "pending"),
        data.get("deadline", None)
    )
    return jsonify({"message": "Task created", "id": task_id}), 201


@tasks_bp.route("/", methods=["GET"])
def get_tasks():
    tasks = db_utils.get_all_tasks()
    return jsonify(tasks)


@tasks_bp.route("/<int:id>", methods=["GET"])
def get_task(id):
    task = db_utils.get_task_by_id(id)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404


@tasks_bp.route("/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.json
    db_utils.update_task(
        id,
        data["title"],
        data.get("description", ""),
        data.get("status", "pending"),
        data.get("deadline", None)
    )
    return jsonify({"message": "Task updated"})


@tasks_bp.route("/<int:id>", methods=["DELETE"])
def delete_task(id):
    db_utils.delete_task(id)
    return jsonify({"message": "Task deleted"})


@tasks_bp.route("/<int:task_id>/notes/<int:note_id>", methods=["POST"])
def add_note_to_task(task_id, note_id):
    db_utils.add_note_to_task(task_id, note_id)
    return jsonify({"message": "Note added to task"})


@tasks_bp.route("/<int:task_id>/notes/<int:note_id>", methods=["DELETE"])
def remove_note_from_task(task_id, note_id):
    db_utils.remove_note_from_task(task_id, note_id)
    return jsonify({"message": "Note removed from task"})