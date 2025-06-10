from skyfield.api import load, wgs84, EarthSatellite

def get_satellite(tle1, tle2, name):
    ts = load.timescale()
    satellite = EarthSatellite(tle1, tle2, name, ts)
    return satellite, ts

def get_az_el_dist(satellite, observer, ts):
    t = ts.now()
    difference = satellite - observer
    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()
    return t.utc_datetime(), az.degrees, alt.degrees, distance.km
