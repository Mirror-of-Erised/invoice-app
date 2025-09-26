from __future__ import annotations

from app.config.settings import settings
from app.db.session import SessionLocal
from app.repositories.sql.customer_repo import CustomerRepoSQL
from app.repositories.sql.invoice_repo import InvoiceRepoSQL
from app.repositories.memory.customer_repo import CustomerRepoMemory
from app.repositories.memory.invoice_repo import InvoiceRepoMemory


def get_repos():
    if settings.use_sql_repos:
        db = SessionLocal()
        return {
            "customers": CustomerRepoSQL(db),
            "invoices": InvoiceRepoSQL(db),
            "_db": db,
        }
    else:
        return {
            "customers": CustomerRepoMemory(),
            "invoices": InvoiceRepoMemory(),
        }
