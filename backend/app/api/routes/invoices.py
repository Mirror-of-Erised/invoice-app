from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db

router = APIRouter()

DB_DEP = Depends(get_db)  # avoid B008


@router.get("/invoices")
def list_invoices(db: Session = DB_DEP):
    rows = db.execute(
        text("SELECT invoice_number, total FROM invoices ORDER BY invoice_number")
    ).all()
    return [{"invoice_number": r[0], "total": str(r[1])} for r in rows]
