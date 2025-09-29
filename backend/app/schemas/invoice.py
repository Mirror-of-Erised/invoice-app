# backend/app/schemas/invoice.py
from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


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
    number: str
    customer_id: UUID
    organization_id: Optional[UUID] = None
    issue_date: date
    due_date: Optional[date] = None
    status: str = "draft"
    subtotal: Optional[Decimal] = Decimal("0")
    tax_total: Optional[Decimal] = Decimal("0")
    total: Decimal


class InvoiceCreate(InvoiceBase):
    line_items: List[InvoiceLineItemCreate] = []


class InvoiceUpdate(BaseModel):
    # all fields optional for PATCH/PUT semantics; adjust if you require stricter behavior
    number: Optional[str] = None
    customer_id: Optional[UUID] = None
    organization_id: Optional[UUID] = None
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    subtotal: Optional[Decimal] = None
    tax_total: Optional[Decimal] = None
    total: Optional[Decimal] = None
    line_items: Optional[List[InvoiceLineItemCreate]] = None


class InvoiceOut(InvoiceBase):
    id: UUID
    line_items: List[InvoiceLineItemOut] = []

    model_config = ConfigDict(from_attributes=True)
