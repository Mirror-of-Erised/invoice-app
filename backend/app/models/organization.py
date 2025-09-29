from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import uuid

if TYPE_CHECKING:
    from .customer import Customer
    from .invoice import Invoice  # <-- add for typing only


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    # MUST be typed for SQLAlchemy 2.0
    invoices: Mapped[list["Invoice"]] = relationship(
        "Invoice",
        back_populates="organization",
        cascade="save-update, merge",
    )

    customers: Mapped[list["Customer"]] = relationship(
        "Customer",
        back_populates="organization",
        cascade="save-update, merge",
    )
