import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import APP_ENV
from src.providers.cache import cache
from src.routers.iss import router as iss_router

app = FastAPI(title="Satellite Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(iss_router)

@app.on_event("startup")
async def startup():
    cache.get_tle(25544)
    print(f"Backend running ({APP_ENV})")

@app.get("/health")
async def health():
    return {'status': 'ok', 'env': APP_ENV}
