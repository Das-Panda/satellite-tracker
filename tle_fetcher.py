import requests

def get_tle_by_name(name, url):
    """Fetches TLE data for a specific satellite from a Celestrak URL."""
    response = requests.get(url)
    lines = response.text.strip().splitlines()
    for i, line in enumerate(lines):
        if name.upper() in line.upper():
            return line, lines[i+1], lines[i+2]
    raise Exception(f"TLE for {name} not found at {url}")
