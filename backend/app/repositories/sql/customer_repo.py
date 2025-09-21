from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.customer import Customer

class SqlCustomerRepo:
    def __init__(self, session: Session):
        self.session = session

    def list(self, organization_id: Optional[str] = None) -> list[dict]:
        stmt = select(Customer)
        if organization_id:
            stmt = stmt.where(Customer.organization_id == organization_id)
        rows = self.session.scalars(stmt).all()
        return [self._to_dict(r) for r in rows]

    def get(self, cid: str) -> Optional[dict]:
        row = self.session.get(Customer, cid)
        return self._to_dict(row) if row else None

    def create(self, data: dict) -> dict:
        obj = Customer(**data)
        self.session.add(obj)
        self.session.flush()
        return self._to_dict(obj)

    @staticmethod
    def _to_dict(c: Customer) -> dict:
        return {
            "id": str(c.id),
            "organization_id": str(c.organization_id),
            "name": c.name,
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "updated_at": c.updated_at.isoformat() if c.updated_at else None,
        }