from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import uuid


if TYPE_CHECKING:
    from .organization import Organization
    from .invoice import Invoice


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    organization_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("organizations.id"), nullable=True)

    organization: Mapped["Organization | None"] = relationship(
        "Organization",
        back_populates="customers",
    )

    invoices: Mapped[list["Invoice"]] = relationship(
        "Invoice",
        back_populates="customer",
        cascade="save-update, merge",
    )
