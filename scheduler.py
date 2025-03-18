from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from organizer import organize_files
import os
import json

scheduler = BackgroundScheduler(daemon=True)
SCHEDULE_FILE = "schedule.json"

def scheduled_task(source_folder, destination_folder, rules):
    """Function that runs at scheduled intervals to organize files."""
    print("Running scheduled file organization...")
    if os.path.exists(source_folder) and os.path.exists(destination_folder):
        organize_files(source_folder, destination_folder, rules)
        print("Files organized successfully!")
    else:
        print("Source or destination folder does not exist.")

def save_schedule(source_folder, destination_folder, rules, interval_minutes):
    """Save scheduled task settings to a JSON file."""
    schedule_data = {
        "source_folder": source_folder,
        "destination_folder": destination_folder,
        "rules": rules,
        "interval_minutes": interval_minutes
    }
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(schedule_data, f)

def load_schedule():
    """Load and restore the scheduled task if it exists."""
    if os.path.exists(SCHEDULE_FILE):
        try:
            with open(SCHEDULE_FILE, "r") as f:
                schedule_data = json.load(f)
                source_folder = schedule_data["source_folder"]
                destination_folder = schedule_data["destination_folder"]
                rules = schedule_data["rules"]
                interval_minutes = schedule_data["interval_minutes"]

                # Restart the scheduler with saved settings
                schedule_task(source_folder, destination_folder, rules, interval_minutes)
                print(f"✅ Restored schedule: every {interval_minutes} minutes.")
        except Exception as e:
            print(f"⚠️ Error loading schedule: {e}")

def schedule_task(source_folder, destination_folder, rules, interval_minutes):
    """Schedule a new task and save it."""
    job_id = "file_organizer_job"

    # Remove any existing job
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    # Schedule the new job
    scheduler.add_job(
        scheduled_task,
        trigger=IntervalTrigger(minutes=interval_minutes),
        args=[source_folder, destination_folder, rules],
        id=job_id,
        replace_existing=True,
        misfire_grace_time=60
    )

    # Save schedule to file
    save_schedule(source_folder, destination_folder, rules, interval_minutes)

def start_scheduler():
    """Start the scheduler and load any saved schedule."""
    if not scheduler.running:
        scheduler.start()
        load_schedule()  # Restore schedule on startup