# -Flask-Task-Tracker
# Sobhi's Flask Task Tracker

A simple web application built with Flask to demonstrate backend fundamentals:

- Basic CRUD with JSON file storage
- Clean Bootstrap-based UI

## What this app does

This is a personal task tracker for Sobhi. You can:

- add tasks
- search tasks
- edit tasks
- delete tasks
- keep everything stored in `data/tasks.json`

## Run locally

1. Create and activate a virtual environment.

4. Open `http://127.0.0.1:5000`

## Quick start in this workspace

If you want the easiest option in this folder, run:

```powershell
.\run_app.bat
```

Then open `http://127.0.0.1:5000`

## How to use it

1. Open the app in your browser.
2. Fill in the task form on the left and click `Create Task`.
3. Use the search box to filter tasks by title or description.
4. Click `Edit` to update a task.
5. Click `Delete` to remove a task.

## Where your data lives

- App code: `app.py`
- Templates: `templates/`
- Styling: `static/css/styles.css`
- Saved tasks: `data/tasks.json`

## Routes

- `/` redirects to `/tasks`
