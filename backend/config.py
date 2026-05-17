from dotenv import load_dotenv
from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT_DIR / ".env"
load_dotenv(ENV_FILE)

APP_ENV = os.getenv("APP_ENV")
DATABASE_URL = os.getenv("DATABASE_URL")
NASA_KEY = os.getenv("NASA_KEY")

