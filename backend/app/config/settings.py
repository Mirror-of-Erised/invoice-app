# backend/app/config/settings.py
from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from dotenv import load_dotenv


# Load .env from repo root: invoice-app/.env
ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")


def _to_bool(val: str | None, default: bool = False) -> bool:
    if val is None:
        return default
    return str(val).strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    # app/debug
    debug: bool = _to_bool(os.getenv("DEBUG"), default=True)

    # db
    database_url: str = os.getenv(
        "DATABASE_URL",
        f"postgresql+psycopg2://{os.getenv('USER','postgres')}@localhost:5432/invoice_app",
    )

    # repo backend selection
    # prefer USE_SQL_REPOS=1/true/yes to flip; fallback to REPO_BACKEND if present
    repo_backend: Literal["sql", "memory"] = (
        "sql" if _to_bool(os.getenv("USE_SQL_REPOS", "true"), default=True) else "memory"
    )

    @property
    def use_sql_repos(self) -> bool:
        return self.repo_backend == "sql"


# create a singleton you can import elsewhere
settings = Settings()
