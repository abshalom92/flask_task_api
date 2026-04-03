from flask import Blueprint, jsonify, request
from app.storage import load_tasks, save_tasks

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return jsonify({"message": "Task API is running"})
    
@main.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

@main.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Task text is required"}), 400

    tasks = load_tasks()

    new_task = {
        "id": len(tasks) + 1,
        "text": data["text"],
        "completed": False
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return jsonify(new_task), 201

@main.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            return jsonify(task)

    return jsonify({"error": "Task not found"}), 404

@main.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            return jsonify({"message": "Task deleted"})

    return jsonify({"error": "Task not found"}), 404