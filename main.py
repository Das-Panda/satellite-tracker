from skyfield.api import load, wgs84, EarthSatellite
import requests
from datetime import datetime
import time
import csv
import os

def get_iss_tle():
    """Fetches TLE data for the ISS from Celestrak"""
    url = "https://celestrak.org/NORAD/elements/stations.txt"
    response = requests.get(url)
    lines = response.text.strip().splitlines()

    for i, line in enumerate(lines):
        if "ISS" in line:
            return line, lines[lines.index(line) + 1], lines[lines.index(line) + 2]

    raise Exception("ISS TLE not found.")

def track_iss(lat, lon, alt_m=0):
    print("\n[📡 Real-Time ISS Tracking - Press Ctrl+C to Stop]")

    name, tle1, tle2 = get_iss_tle()
    ts = load.timescale()
    satellite = EarthSatellite(tle1, tle2, name, ts)
    observer = wgs84.latlon(lat, lon, alt_m)

    log_file = "logs/tracking_log.csv"

    # Create log file with headers if it doesn't exist
    if not os.path.exists(log_file):
        with open(log_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp (UTC)", "Azimuth (deg)", "Elevation (deg)", "Distance (km)"])

    try:
        while True:
            t = ts.now()
            difference = satellite - observer
            topocentric = difference.at(t)

            alt, az, distance = topocentric.altaz()

            print(f"\n🕒 {t.utc_datetime():%Y-%m-%d %H:%M:%S} UTC")
            print(f"Azimuth:     {az.degrees:.2f}°")
            print(f"Elevation:   {alt.degrees:.2f}°")
            print(f"Distance:    {distance.km:.2f} km")

            with open(log_file, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    t.utc_datetime().strftime("%Y-%m-%d %H:%M:%S"),
                    f"{az.degrees:.2f}",
                    f"{alt.degrees:.2f}",
                    f"{distance.km:.2f}"
                ])

            time.sleep(10)

    except KeyboardInterrupt:
        print("\n❌ Tracking stopped by user.")

if __name__ == "__main__":
    print("Enter your ground station location:")
    lat = float(input("Latitude (e.g. 33.2): "))
    lon = float(input("Longitude (e.g. -97.1): "))
    alt = float(input("Altitude in meters (optional, default=0): ") or "0")

    track_iss(lat, lon, alt)
