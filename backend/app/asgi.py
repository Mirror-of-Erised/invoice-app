from __future__ import annotations

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.customers import router as customers_router
from app.api.invoices import router as invoices_router

app = FastAPI()

# Mount FastAPI routers under /api
app.include_router(health_router, prefix="/api")
app.include_router(customers_router, prefix="/api")
app.include_router(invoices_router, prefix="/api")
