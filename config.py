import os

APP_CONFIG = os.getenv("APP_CONFIG", "production")
BASE_DIR = os.getenv("BASE_DIR", os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.getenv("DATA_DIR", os.path.join(BASE_DIR, "data"))
TEMPLATES_DIR = os.getenv("TEMPLATES_DIR", os.path.join(BASE_DIR, "templates"))
ZIP_DIR = os.getenv("ZIP_DIR", os.path.join(DATA_DIR, "zip"))
CSV_DIR = os.getenv("CSV_DIR", os.path.join(DATA_DIR, "csv"))
HOST = os.getenv("HOST", "0.0.0.0")
PORT = os.getenv("PORT", 5000)
REDIS_HOST = os.getenv("REDIS_URL", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
