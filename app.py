from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from flask import Flask, flash, redirect, render_template, request, url_for


import os

BASE_DIR = Path(__file__).resolve().parent
if os.environ.get("VERCEL"):
    DATA_FILE = Path("/tmp/tasks.json")
else:
    DATA_FILE = BASE_DIR / "data" / "tasks.json"

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"


def load_tasks() -> list[dict[str, Any]]:
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_tasks(tasks: list[dict[str, Any]]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)


def get_next_id(tasks: list[dict[str, Any]]) -> int:
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


@app.route("/")
def home():
    return redirect(url_for("task_list"))


@app.route("/tasks", methods=["GET", "POST"])
def task_list():
    tasks = load_tasks()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "Pending")

        if not title:
            flash("Task title is required.", "danger")
        else:
            tasks.append(
                {
                    "id": get_next_id(tasks),
                    "title": title,
                    "description": description,
                    "status": status,
                }
            )
            save_tasks(tasks)
            flash("Task created successfully.", "success")
            return redirect(url_for("task_list"))

    query = request.args.get("q", "").strip().lower()
    filtered_tasks = tasks
    if query:
        filtered_tasks = [
            task
            for task in tasks
            if query in task["title"].lower() or query in task["description"].lower()
        ]

    return render_template("tasks.html", tasks=filtered_tasks, query=query)


@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id: int):
    tasks = load_tasks()
    task = next((item for item in tasks if item["id"] == task_id), None)

    if task is None:
        flash("Task not found.", "danger")
        return redirect(url_for("task_list"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "Pending")

        if not title:
            flash("Task title is required.", "danger")
        else:
            task["title"] = title
            task["description"] = description
            task["status"] = status
            save_tasks(tasks)
            flash("Task updated successfully.", "success")
            return redirect(url_for("task_list"))

    return render_template("edit_task.html", task=task)


@app.post("/tasks/<int:task_id>/delete")
def delete_task(task_id: int):
    tasks = load_tasks()
    updated_tasks = [task for task in tasks if task["id"] != task_id]

    if len(updated_tasks) == len(tasks):
        flash("Task not found.", "danger")
    else:
        save_tasks(updated_tasks)
        flash("Task deleted successfully.", "warning")

    return redirect(url_for("task_list"))


if __name__ == "__main__":
    app.run(debug=True)
