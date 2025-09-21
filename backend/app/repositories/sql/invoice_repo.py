from __future__ import annotations
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.invoice import Invoice

class SqlInvoiceRepo:
    def __init__(self, session: Session):
        self.session = session

    def list(self, organization_id: Optional[str] = None, customer_id: Optional[str] = None):
        stmt = select(Invoice)
        if organization_id:
            stmt = stmt.where(Invoice.organization_id == organization_id)
        if customer_id:
            stmt = stmt.where(Invoice.customer_id == customer_id)
        rows = self.session.scalars(stmt).all()
        return [self._to_dict(r) for r in rows]

    def create(self, data: dict) -> dict:
        obj = Invoice(**data)
        self.session.add(obj)
        self.session.flush()
        return self._to_dict(obj)

    @staticmethod
    def _to_dict(i: Invoice) -> dict:
        return {
            "id": i.id,
            "organization_id": i.organization_id,
            "customer_id": i.customer_id,
            "number": i.number,
            "issue_date": i.issue_date.isoformat() if i.issue_date else None,
            "due_date": i.due_date.isoformat() if i.due_date else None,
            "status": i.status,
            "subtotal": float(i.subtotal or 0),
            "tax": float(i.tax or 0),
            "total": float(i.total or 0),
            "created_at": i.created_at.isoformat() if i.created_at else None,
            "updated_at": i.updated_at.isoformat() if i.updated_at else None,
        }
