from dataclasses import dataclass
import os
from pathlib import Path

# Resolve repo root no matter where Python is launched from
# .../invoice-app/backend/app/config/settings.py -> parents[3] == repo root
ROOT_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT_DIR / ".data"
DATA_DIR.mkdir(exist_ok=True)

DEFAULT_SQLITE = f"sqlite+pysqlite:///{(DATA_DIR / 'dev.sqlite3').as_posix()}"

@dataclass
class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", DEFAULT_SQLITE)
    ECHO_SQL: bool   = os.getenv("ECHO_SQL", "false").lower() == "true"

settings = Settings()

def load_config():
    """Compatibility shim for older imports."""
    return settings
