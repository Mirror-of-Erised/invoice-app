# app/models/invoice.py
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String(36), primary_key=True, nullable=False,
                default=lambda: str(uuid.uuid4()))
    organization_id = Column(String(36), ForeignKey("organizations.id"), nullable=False)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)

    number = Column(String(64), nullable=False)
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date)
    status = Column(String(32), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    tax = Column(Numeric(10, 2), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    # <-- These names must match the back_populates on the other models
    organization = relationship("Organization", back_populates="invoices")
    customer = relationship("Customer", back_populates="invoices")

    line_items = relationship(
        "InvoiceLineItem",
        back_populates="invoice",
        cascade="all, delete-orphan",
    )
