import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String(36), primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # already have this one (from earlier):
    customers = relationship("Customer", back_populates="organization", cascade="all, delete-orphan")

    # add this:
    invoices = relationship("Invoice", back_populates="organization", cascade="all, delete-orphan")
