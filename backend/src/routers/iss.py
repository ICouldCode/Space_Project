from fastapi import APIRouter, HTTPException
from src.providers.cache import cache
from src.services.orbital import OrbitalService

ISS_CAT_NR = 25544
router = APIRouter(prefix="/iss")

@router.get("", include_in_schema=True)
async def iss_position():
    try:
        satellite = cache.get_tle(ISS_CAT_NR)
        return OrbitalService.get_position(satellite)
    except Exception as e:
        print(f"{e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/track")
async def iss_track():
    try:
        satellite = cache.get_tle(ISS_CAT_NR)
        return OrbitalService.get_track(satellite)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
