from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from app.db.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .customer import Customer  # type-only import (no runtime cycle)


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String, nullable=False)

    # use forward-ref in the list element
    customers: Mapped[list["Customer"]] = relationship(
        "Customer", back_populates="organization", cascade="all, delete-orphan"
    )
