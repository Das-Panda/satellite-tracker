import csv
from datetime import datetime
import matplotlib.pyplot as plt

timestamps = []
elevations = []

with open("logs/tracking_log.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Parse timestamp and elevation
        timestamps.append(datetime.strptime(row["Timestamp (UTC)"], "%Y-%m-%d %H:%M:%S"))
        elevations.append(float(row["Elevation (deg)"]))

# Create the plot
plt.figure(figsize=(10, 5))
plt.plot(timestamps, elevations, marker='o', linestyle='-', color='blue')
plt.title("ISS Elevation Over Time")
plt.xlabel("Time (UTC)")
plt.ylabel("Elevation (degrees)")
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)

plt.show()
