from sqlalchemy.orm import Session
from typing import Sequence, Optional
from uuid import UUID
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int = 100, offset: int = 0) -> Sequence[Customer]:
        return self.db.query(Customer).offset(offset).limit(limit).all()

    def get(self, id: UUID) -> Optional[Customer]:
        return self.db.get(Customer, id)

    def create(self, data: CustomerCreate) -> Customer:
        obj = Customer(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, id: UUID, data: CustomerUpdate) -> Optional[Customer]:
        obj = self.get(id)
        if not obj:
            return None
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: UUID) -> bool:
        obj = self.get(id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
