import math
from skyfield.api import load

eph = load('de421.bsp')

class OrbitalService:

    @staticmethod
    def get_position(satellite):
        from providers.cache import ts
        t          = ts.now()
        geocentric = satellite.at(t)
        subpoint   = geocentric.subpoint()

        pos, vel  = geocentric.frame_xyz_and_velocity(geocentric.frame)
        speed_kms = math.sqrt(
            vel[0].km_per_s**2 +
            vel[1].km_per_s**2 +
            vel[2].km_per_s**2
        )

        MU         = 398600.4418
        a          = (MU / (2 * math.pi / satellite.model.no_kozai * (1/60))**2) ** (1/3)
        period_min = 2 * math.pi * math.sqrt(a**3 / MU) / 60

        sunlit = satellite.at(t).is_sunlit(eph)

        return {
            'latitude':    round(subpoint.latitude.degrees, 6),
            'longitude':   round(subpoint.longitude.degrees, 6),
            'altitude_km': round(subpoint.elevation.km, 2),
            'speed_kms':   round(speed_kms, 4),
            'period_min':  round(period_min, 2),
            'sunlit':      bool(sunlit),
            'timestamp':   t.utc_iso(),
        }

    @staticmethod
    def get_track(satellite, minutes=90):
        from providers.cache import ts
        now    = ts.now()
        points = []

        for m in range(0, minutes):
            t          = ts.tt_jd(now.tt + m / 1440.0)
            geocentric = satellite.at(t)
            subpoint   = geocentric.subpoint()
            points.append({
                'lat':              round(subpoint.latitude.degrees, 4),
                'lon':              round(subpoint.longitude.degrees, 4),
                'minutes_from_now': m,
            })

        return {'track': points}