import sys
import os
import time
from skyfield.api import wgs84

# Ensure local modules load correctly
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from tracker.tle_parser import fetch_tle_list
from tracker.logger import create_log_path, initialize_log, log_tracking_data
from tracker.position import get_satellite, get_az_el_dist

def main():
    print("Enter your ground station location:")
    lat = float(input("Latitude (e.g. 33.2): "))
    lon = float(input("Longitude (e.g. -97.1): "))
    alt = float(input("Altitude in meters (optional, default=0): ") or "0")

    # --- Load TLEs from Celestrak (Amateur satellites list)
    tle_url = "https://celestrak.org/NORAD/elements/amateur.txt"
    all_sats = fetch_tle_list(tle_url)

    print("\nSelect a satellite to track:")
    for idx, (name, _, _) in enumerate(all_sats[:20], start=1):  # Show only first 20
        print(f"{idx}. {name}")

    choice = input("Enter satellite number (1-20): ").strip()
    try:
        index = int(choice) - 1
        satellite_name, tle1, tle2 = all_sats[index]
    except (ValueError, IndexError):
        print("Invalid choice. Defaulting to first satellite.")
        satellite_name, tle1, tle2 = all_sats[0]

    print(f"\nTracking: {satellite_name}")

    # --- Create unique session log file
    log_file = create_log_path(satellite_name)
    initialize_log(log_file)

    # --- Load satellite and prepare observer
    satellite, ts = get_satellite(tle1, tle2, satellite_name)
    observer = wgs84.latlon(lat, lon, alt)

    print("\n[📡 Real-Time Satellite Tracking - Press Ctrl+C to Stop]")

    try:
        while True:
            timestamp, azimuth, elevation, distance = get_az_el_dist(satellite, observer, ts)

            print(f"\n🕒 {timestamp:%Y-%m-%d %H:%M:%S} UTC")
            print(f"Azimuth:     {azimuth:.2f}°")
            print(f"Elevation:   {elevation:.2f}°")
            print(f"Distance:    {distance:.2f} km")

            log_tracking_data(
                log_file,
                timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                f"{azimuth:.2f}",
                f"{elevation:.2f}",
                f"{distance:.2f}"
            )

            time.sleep(10)

    except KeyboardInterrupt:
        print(f"\n❌ Tracking stopped. Data saved to {log_file}")

if __name__ == "__main__":
    main()
