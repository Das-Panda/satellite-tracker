import os
import csv
from datetime import datetime
from re import sub

def create_log_path(satellite_name):
    """Creates a satellite-specific folder and log filename with timestamp."""
    # Make satellite name safe for folder names
    safe_name = sub(r'[^\w\-_\. ]', '_', satellite_name)
    log_folder = os.path.join("logs", safe_name)

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Timestamp for filename
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H%MUTC")
    filename = f"{timestamp}.csv"

    return os.path.join(log_folder, filename)

def initialize_log(log_file):
    """Creates a CSV file with headers if it doesn't exist."""
    with open(log_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp (UTC)", "Azimuth (deg)", "Elevation (deg)", "Distance (km)"])

def log_tracking_data(log_file, timestamp, azimuth, elevation, distance):
    """Appends tracking data to the CSV log."""
    with open(log_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, azimuth, elevation, distance])
