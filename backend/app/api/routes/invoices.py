# backend/app/api/invoices.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db import get_db
from app.repos.invoices_sql import InvoiceRepo
from app.schemas.invoice import InvoiceCreate, InvoiceOut, InvoiceLineItemCreate, InvoiceLineItemOut

router = APIRouter(prefix="/api/invoices", tags=["invoices"])


@router.get("", response_model=list[InvoiceOut])
def list_invoices(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    return InvoiceRepo(db).list(limit=limit, offset=offset)


@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(invoice_id: UUID, db: Session = Depends(get_db)):
    inv = InvoiceRepo(db).get(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv


@router.post("", response_model=InvoiceOut, status_code=status.HTTP_201_CREATED)
def create_invoice(payload: InvoiceCreate, db: Session = Depends(get_db)):
    try:
        return InvoiceRepo(db).create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # handle duplicate number -> 409
        msg = str(e)
        if "uq_invoices_number" in msg or "already exists" in msg or "duplicate key value" in msg:
            raise HTTPException(status_code=409, detail="Invoice number already exists")
        raise


# ----- line items -----
@router.post("/{invoice_id}/line-items", response_model=InvoiceLineItemOut, status_code=status.HTTP_201_CREATED)
def add_line_item(invoice_id: UUID, payload: InvoiceLineItemCreate, db: Session = Depends(get_db)):
    repo = InvoiceRepo(db)
    item = repo.add_line_item(invoice_id, payload.description, payload.qty, payload.unit_price)
    if item is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return item


@router.get("/{invoice_id}/line-items", response_model=list[InvoiceLineItemOut])
def list_line_items(invoice_id: UUID, db: Session = Depends(get_db)):
    return InvoiceRepo(db).list_line_items(invoice_id)
