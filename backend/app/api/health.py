from __future__ import annotations
from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("health")
@router.get("/health")
def health():
    return {"status": "ok"}
