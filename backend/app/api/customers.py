from __future__ import annotations

from typing import Annotated, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db

DB = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/customers", tags=["customers"])

# Define the param annotations WITHOUT defaults inside Query(...)
OrgId = Annotated[Optional[str], Query()]                 # default via '= None'
Limit = Annotated[int, Query(ge=1, le=200)]               # default via '= 50'


@router.get("")
@router.get("/")
def list_customers(
    db: DB,
    organization_id: OrgId = None,    # default set here
    limit: Limit = 50,                # default set here
):
    rows = db.execute(
        text(
            """
            SELECT id, organization_id, name, email, created_at, updated_at
            FROM customers
            WHERE (:org IS NULL OR organization_id = :org)
            ORDER BY created_at DESC
            LIMIT :limit
            """
        ),
        {"org": organization_id, "limit": limit},
    ).mappings().all()
    return rows


@router.post("", status_code=201)
@router.post("/", status_code=201)
def create_customer(db: DB, payload: dict[str, Any]):
    row = db.execute(
        text(
            """
            INSERT INTO customers (organization_id, name, email)
            VALUES (:org, :name, :email)
            RETURNING id, organization_id, name, email, created_at, updated_at
            """
        ),
        {
            "org": payload.get("organization_id"),
            "name": payload.get("name"),
            "email": payload.get("email"),
        },
    ).mappings().one()
    db.commit()
    return row


@router.get("/{cid}")
def get_customer(cid: str, db: DB):
    row = db.execute(
        text(
            """
            SELECT id, organization_id, name, email, created_at, updated_at
            FROM customers
            WHERE id = :id
            """
        ),
        {"id": cid},
    ).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="not found")
    return row
