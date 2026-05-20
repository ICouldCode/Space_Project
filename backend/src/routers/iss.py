from fastapi import APIRouter, HTTPException
from src.providers.cache import cache
from src.services.orbital import OrbitalService
from src.providers.celestrak.satellites import ISS

router = APIRouter(prefix="/iss")
@router.get("")
async def iss_position():
    try:
        satellite = cache.get_tle(ISS.CAT_NR)
        position = OrbitalService.get_position(satellite)
        position['feed'] = ISS.FEED
        return position
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/track")
async def iss_track():
    try:
        satellite = cache.get_tle(ISS.CAT_NR)
        return OrbitalService.get_track(satellite)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
