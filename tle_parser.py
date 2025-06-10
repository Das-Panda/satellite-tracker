import requests

def fetch_tle_list(url):
    """Fetches all TLE sets from a given Celestrak TLE URL and returns a list of (name, tle1, tle2) tuples."""
    response = requests.get(url)
    lines = response.text.strip().splitlines()

    satellites = []
    for i in range(0, len(lines), 3):
        name = lines[i].strip()
        tle1 = lines[i + 1].strip()
        tle2 = lines[i + 2].strip()
        satellites.append((name, tle1, tle2))

    return satellites
