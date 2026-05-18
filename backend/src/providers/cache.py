import time
from providers.celestrak.satellite import Satellite
from skyfield.api import load, EarthSatellite

ts = load.timescale()

class TLECache:
    def __init__(self, ttl=21600):
        self._cache = {}
        self._ttl = ttl

    def get_tle(self, cat_nr):
        now = time.time()
        entry = self._cache.get(cat_nr)
        if entry is None or now - entry['fetched_at'] > self._ttl:
            print(f"Fetching fresh TLE for {cat_nr}...")
            name, line1, line2 = Satellite.get_tle_num(cat_nr)
            self._cache[cat_nr] = {
                'satellite': EarthSatellite(line1, line2, name, ts),
                'fetched_at': now,
            }
            print(f"TLE loaded: {name}")
        return self._cache[cat_nr]['satellite']