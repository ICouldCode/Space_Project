import time
from skyfield.api import load, EarthSatellite
from src.providers.celestrak.satellite import Satellite
from src.database.repositories.tle_repository import TLERepo

ts = load.timescale()
tleRepo = TLERepo()

class TLECache:
    def __init__(self, ttl=21600):
        self._cache = {}
        self._ttl = ttl

    @staticmethod
    def _build_satellite(db_row):
        _, name, line1, line2, fetched_at = db_row
        return EarthSatellite(line1, line2, name, ts)

    def get_tle(self, cat_nr):
        now = time.time()

        entry = self._cache.get(cat_nr)
        if entry and now - entry['fetched_at'] <= self._ttl:
            return entry['satellite']

        db_pull = tleRepo.get_latest(cat_nr)
        if db_pull:
            _,  _, name, line1, line2, fetched_at = db_pull
            if now - fetched_at.timestamp() <= self._ttl:
                self._cache[cat_nr] = {
                    'satellite': EarthSatellite(line1, line2, name, ts),
                    'fetched_at': fetched_at.timestamp()
                }
                return self._cache[cat_nr]['satellite']

        print(f"Fetching fresh TLE for {cat_nr}...")
        name, line1, line2 = Satellite.get_tle_num(cat_nr)
        tleRepo.insert(cat_nr, name, line1, line2)
        self._cache[cat_nr] = {
            'satellite': EarthSatellite(line1, line2, name, ts),
            'fetched_at': now,
        }
        print(f"TLE loaded: {name}")
        return self._cache[cat_nr]['satellite']
    
cache = TLECache()
