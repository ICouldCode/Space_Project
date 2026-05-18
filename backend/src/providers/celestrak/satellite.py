import urllib.request
from providers.celestrak.urls import BASE_URL, TLE_URL

class Satellite:

    @staticmethod
    def get_tle_name(name):
        with urllib.request.urlopen(TLE_URL) as response:
            lines = response.read().decode('utf-8').splitlines()
        for i, line in enumerate(lines):
            if name in line:
                return line.strip(), lines[i+1].strip(), lines[i+2].strip()
        raise ValueError(f"{name} TLE not found in Celestrak response")

    @staticmethod
    def get_tle_num(cat_nr):
        url = f"{BASE_URL}CATNR={cat_nr}&FORMAT=TLE"
        with urllib.request.urlopen(url) as response:
            lines = response.read().decode('utf-8').splitlines()
        lines = [l.strip() for l in lines if l.strip()]
        return lines[0], lines[1], lines[2]