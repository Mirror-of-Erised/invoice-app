from fastapi import FastAPI, Depends
from starlette.middleware.wsgi import WSGIMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import SessionLocal
from app.flask_app import create_flask_app

# ---- FastAPI part (our new /invoices route) ----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

fastapi_app = FastAPI()

@fastapi_app.get("/invoices")
def list_invoices(db: Session = Depends(get_db)):
    rows = db.execute(text(
        "SELECT invoice_number, total FROM invoices ORDER BY invoice_number"
    )).all()
    return [{"invoice_number": r[0], "total": str(r[1])} for r in rows]

# ---- Compose FastAPI + Flask under a single ASGI app ----
app = FastAPI()
app.mount("/flask", WSGIMiddleware(create_flask_app()))  # your existing Flask routes at /flask/...
app.mount("/", fastapi_app)                               # FastAPI at /
