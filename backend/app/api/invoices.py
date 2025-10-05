from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from sqlalchemy.exc import IntegrityError
from app.db.session import get_db
from app.repos.invoices_sql import InvoiceRepo
from app.schemas.invoice import InvoiceOut, InvoiceCreate, InvoiceUpdate


router = APIRouter(prefix="/api/invoices", tags=["invoices"])


def _normalize_invoice_out(obj) -> InvoiceOut:
    """
    Ensure `invoice_number` is always a non-null string for response validation.
    Falls back to legacy `number` if `invoice_number` is None.
    Works with ORM instances or dict-like objects that Pydantic can validate from.
    """
    # First, build the pydantic model from the object
    model = InvoiceOut.model_validate(obj)
    if model.invoice_number is None or model.invoice_number == "":
        # Try to read legacy `.number` off the original object (ORM attr or dict key)
        legacy = getattr(obj, "number", None)
        if legacy is None and isinstance(obj, dict):
            legacy = obj.get("number")
        # Update the model with the fallback if present
        if legacy:
            model = model.model_copy(update={"invoice_number": legacy})
    return model


@router.get("", response_model=List[InvoiceOut])
def list_invoices(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    objs = InvoiceRepo(db).list(limit=limit, offset=offset)
    # Coalesce at the boundary so response_model validation never sees a null
    return [_normalize_invoice_out(o) for o in objs]


@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(invoice_id: UUID, db: Session = Depends(get_db)):
    obj = InvoiceRepo(db).get(invoice_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return _normalize_invoice_out(obj)


@router.post("", response_model=InvoiceOut, status_code=status.HTTP_201_CREATED)
def create_invoice(payload: InvoiceCreate, db: Session = Depends(get_db)):
    try:
        obj = InvoiceRepo(db).create(payload)
    except IntegrityError:
        # keep the session usable for subsequent requests
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="invoice_number already exists in this organization",
        )
    return _normalize_invoice_out(obj)


@router.patch("/{invoice_id}", response_model=InvoiceOut)
def update_invoice(invoice_id: UUID, payload: InvoiceUpdate, db: Session = Depends(get_db)):
    obj = InvoiceRepo(db).update(invoice_id, payload)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return _normalize_invoice_out(obj)


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(invoice_id: UUID, db: Session = Depends(get_db)):
    ok = InvoiceRepo(db).delete(invoice_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
