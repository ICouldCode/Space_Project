from src.providers.celestrak.satellite import Satellite

class ISS(Satellite):
    CAT_NR = 25544
    NAME = 'ISS (ZARYA)'
    FEED = "https://www.youtube.com/embed/FuuC4dpSQ1M?autoplay=1"
