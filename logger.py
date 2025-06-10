import os
import csv

def initialize_log(log_file):
    if not os.path.exists(log_file):
        with open(log_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp (UTC)", "Azimuth (deg)", "Elevation (deg)", "Distance (km)"])

def log_tracking_data(log_file, timestamp, azimuth, elevation, distance):
    with open(log_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, azimuth, elevation, distance])
