# backend/app/schemas/invoice.py
from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, model_validator


# ---------- Line Items ----------
class InvoiceLineItemCreate(BaseModel):
    description: str
    qty: Decimal = Field(..., gt=0)  # ORM attr is "qty" (DB column "quantity")
    unit_price: Decimal = Field(..., ge=0)  # ORM attr is "unit_price"


class InvoiceLineItemOut(InvoiceLineItemCreate):
    id: UUID
    total: Decimal  # ORM attr "total" (DB column "line_total")

    model_config = ConfigDict(from_attributes=True)


# ---------- Invoices ----------
class InvoiceBase(BaseModel):
    invoice_number: str
    customer_id: UUID
    total: float

    # Make dates optional and fill them via validator
    issue_date: Optional[date] = None
    due_date: Optional[date] = None

    currency: str = "USD"
    status: str = "draft"  # or Literal[...] if you already use it
    notes: Optional[str] = None

    @model_validator(mode="after")
    def _fill_dates(self) -> "InvoiceBase":
        # default issue_date to today
        if self.issue_date is None:
            self.issue_date = date.today()
        # default due_date to +30 days from issue_date
        if self.due_date is None:
            self.due_date = self.issue_date + timedelta(days=30)
        return self


class InvoiceCreate(InvoiceBase):
    """Fields required to create an invoice.

    We inherit the optional dates/currency defaults from InvoiceBase so clients
    can omit them.
    """

    pass


class InvoiceUpdate(BaseModel):
    """All fields optional for PATCH/PUT; no arithmetic at class level."""

    invoice_number: Optional[str] = None
    customer_id: Optional[UUID] = None
    total: Optional[float] = None
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

    @model_validator(mode="after")
    def _normalize_dates(self) -> "InvoiceUpdate":
        # If issue_date provided but due_date omitted, infer +30 days
        if self.issue_date and not self.due_date:
            self.due_date = self.issue_date + timedelta(days=30)
        return self


class InvoiceOut(InvoiceBase):
    id: UUID
    line_items: List[InvoiceLineItemOut] = []

    model_config = ConfigDict(from_attributes=True)
