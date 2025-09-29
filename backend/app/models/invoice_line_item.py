# backend/app/models/invoice_line_item.py
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Numeric, ForeignKey
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base  # <-- ensure this import path is correct


class InvoiceLineItem(Base):
    __tablename__ = "invoice_line_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False, index=True)

    description = Column(String(500), nullable=False)
    qty = Column("quantity", Numeric(12, 2), nullable=False)  # <-- maps to DB column quantity
    unit_price = Column(Numeric(12, 2), nullable=False)
    total = Column("line_total", Numeric(12, 2), nullable=False)  # <-- maps to DB column line_total

    invoice = relationship("Invoice", back_populates="line_items")
