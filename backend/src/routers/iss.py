from fastapi import APIRouter, HTTPException
from main import cache
from services.orbital import OrbitalService

ISS_CAT_NR = 25544
router = APIRouter(prefix="/iss")

@router.get("/")
async def iss_position():
    try:
        satellite = cache.get_tle(ISS_CAT_NR)
        return OrbitalService.get_position(satellite)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/track")
async def iss_track():
    try:
        satellite = cache.get_tle(ISS_CAT_NR)
        return OrbitalService.get_track(satellite)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))