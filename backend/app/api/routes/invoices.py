# backend/app/asgi.py
from __future__ import annotations

from typing import Annotated
from typing import Generator
from fastapi import FastAPI, Depends
from starlette.middleware.wsgi import WSGIMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.flask_app import create_flask_app


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# FastAPI app (ASGI)
fastapi_app = FastAPI()

# Type alias with dependency (avoids B008)
DBSession = Annotated[Session, Depends(get_db)]


@fastapi_app.get("/invoices")
def list_invoices(db: DBSession):
    rows = db.execute(
        text("SELECT invoice_number, total FROM invoices ORDER BY invoice_number")
    ).all()
    return [{"invoice_number": r[0], "total": str(r[1])} for r in rows]


# Compose ASGI app: mount Flask (WSGI) under /flask
app = FastAPI()
app.mount("/flask", WSGIMiddleware(create_flask_app()))
app.mount("/", fastapi_app)
