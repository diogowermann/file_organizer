from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from organizer import organize_files
import os

scheduler = BackgroundScheduler(daemon=True)

def scheduled_task(source_folder, destination_folder, rules):
    """Function that runs at scheduled intervals to organize files."""
    print("Running scheduled file organization...")
    if os.path.exists(source_folder) and os.path.exists(destination_folder):
        organize_files(source_folder, destination_folder, rules)
        print("Files organized successfully!")
    else:
        print("Source or destination folder does not exist.")

def start_scheduler():
    """Start the scheduler (runs in the background)."""
    if not scheduler.running: scheduler.start()
