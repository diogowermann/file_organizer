from flask import Blueprint, render_template, request, jsonify
from organizer import organize_files
import tkinter as tk
from tkinter import filedialog
from scheduler import scheduler, scheduled_task, start_scheduler
from apscheduler.triggers.interval import IntervalTrigger

file_organizer_routes = Blueprint("file_organizer", __name__)

start_scheduler()

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select Folder", parent=root)
    return folder_selected

@file_organizer_routes.route("/select-folder", methods=["GET"])
def select_folder_route():
    folder_path = select_folder()
    return jsonify({"folder": folder_path})

@file_organizer_routes.route("/")
def index():
    return render_template("index.html")

@file_organizer_routes.route("/organize", methods=["POST"])
def organize():
    data = request.json
    source_folder = data.get("source_folder")
    destination_folder = data.get("destination_folder")
    rules = data.get("rules")  # List of rules provided by the user

    if not source_folder or not destination_folder or not rules:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        organize_files(source_folder, destination_folder, rules)
        return jsonify({"message": "Files organized successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@file_organizer_routes.route("/schedule", methods=["POST"])
def schedule_organization():
    data = request.json
    source_folder = data.get("source_folder")
    destination_folder = data.get("destination_folder")
    rules = data.get("rules")
    interval_minutes = int(data.get("interval_minutes", 10))  # Default: 10 minutes

    if not source_folder or not destination_folder or not rules:
        return jsonify({"error": "Missing required fields"}), 400

    job_id = "file_organizer_job"
    
    # Remove any existing job with the same ID
    scheduler.remove_job(job_id, jobstore=None) if scheduler.get_job(job_id) else None

    # Schedule the task
    scheduler.add_job(
        scheduled_task,
        trigger=IntervalTrigger(minutes=interval_minutes),
        args=[source_folder, destination_folder, rules],
        id=job_id,
        replace_existing=True,
        misfire_grace_time=60  # Allow jobs to run up to 60 seconds late
    )

    return jsonify({"message": f"File organization scheduled every {interval_minutes} minutes."}), 200

@file_organizer_routes.route("/cancel-schedule", methods=["POST"])
def cancel_schedule():
    """Cancel the scheduled task if the user wants to stop it."""
    job_id = "file_organizer_job"
    
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        return jsonify({"message": "Scheduled task canceled successfully."}), 200
    else:
        return jsonify({"error": "No active scheduled task found."}), 400