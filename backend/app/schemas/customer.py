from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID


class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=50)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=50)


class CustomerOut(CustomerBase):
    id: UUID

    class Config:
        from_attributes = True  # Pydantic v2: map from SQLAlchemy ORM
