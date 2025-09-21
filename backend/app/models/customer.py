from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from app.db.base import Base

if TYPE_CHECKING:
    from .organization import Organization  # type-only import

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

    organization: Mapped["Organization"] = relationship(back_populates="customers")
