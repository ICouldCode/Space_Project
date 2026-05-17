from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow your frontend to talk to your backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change this to your frontend's specific URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/iss")
def get_iss_location():
    # Pull latest X, Y, Z coordinates from your Postgres DB here
    return {"x": 1.24, "y": -0.85, "z": 2.11}