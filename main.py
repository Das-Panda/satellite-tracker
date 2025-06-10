import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from skyfield.api import wgs84
from tracker.tle_fetcher import get_tle_by_name
from tracker.logger import initialize_log, log_tracking_data
from tracker.position import get_satellite, get_az_el_dist

def main():
    print("Enter your ground station location:")
    lat = float(input("Latitude (e.g. 33.2): "))
    lon = float(input("Longitude (e.g. -97.1): "))
    alt = float(input("Altitude in meters (optional, default=0): ") or "0")

    satellite_name = "ISS (ZARYA)"
    tle_url = "https://celestrak.org/NORAD/elements/stations.txt"
    log_file = "logs/tracking_log.csv"

    # Fetch TLE data
    name, tle1, tle2 = get_tle_by_name(satellite_name, tle_url)

    # Load satellite
    satellite, ts = get_satellite(tle1, tle2, name)
    observer = wgs84.latlon(lat, lon, alt)

    # Initialize CSV log
    initialize_log(log_file)

    print("\n[📡 Real-Time ISS Tracking - Press Ctrl+C to Stop]")

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

            import time
            time.sleep(10)

    except KeyboardInterrupt:
        print("\n❌ Tracking stopped by user.")

if __name__ == "__main__":
    main()
