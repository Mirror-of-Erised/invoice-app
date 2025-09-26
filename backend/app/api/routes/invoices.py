from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware

# your FastAPI invoices route
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import SessionLocal
# import your existing Flask WSGI app
from app.main import app as flask_app  # <- adjust import to wherever your Flask app lives


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


# compose: FastAPI handles /invoices; Flask mounted under /flask (avoid route collisions)
app = FastAPI()
app.mount("/flask", WSGIMiddleware(flask_app))
app.mount("/", fastapi_app)
