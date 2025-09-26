from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db

DB = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("")
@router.get("/")
def list_invoices(db: DB):
    rows = db.execute(text("SELECT invoice_number, total FROM invoices ORDER BY invoice_number")).all()
    return [{"invoice_number": r[0], "total": str(r[1])} for r in rows]
