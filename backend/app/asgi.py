from __future__ import annotations

from fastapi import FastAPI, Depends
from starlette.middleware.wsgi import WSGIMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.flask_app import create_flask_app


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


fastapi_app = FastAPI()

DB_DEP = Depends(get_db)  # avoid B008


@fastapi_app.get("/invoices")
def list_invoices(db: Session = DB_DEP):
    rows = db.execute(
        text("SELECT invoice_number, total FROM invoices ORDER BY invoice_number")
    ).all()
    return [{"invoice_number": r[0], "total": str(r[1])} for r in rows]


app = FastAPI()
app.mount("/flask", WSGIMiddleware(create_flask_app()))
app.mount("/", fastapi_app)
