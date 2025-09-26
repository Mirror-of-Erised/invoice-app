# backend/app/services/container.py
from app.config.settings import settings
from app.db.session import SessionLocal
from app.repositories.sql.customer_repo import CustomerRepoSQL
from app.repositories.sql.invoice_repo  import InvoiceRepoSQL
from app.repositories.memory.customer_repo import CustomerRepoMemory
from app.repositories.memory.invoice_repo  import InvoiceRepoMemory


def get_repos():
    if settings.use_sql_repos:
        db = SessionLocal()
        return {"customers": CustomerRepoSQL(db), "invoices": InvoiceRepoSQL(db), "_db": db}
    else:
        return {"customers": CustomerRepoMemory(), "invoices": InvoiceRepoMemory()}


class RepoContainer:
    """Holds repos and (for SQL) the scoped DB session."""
    def __init__(self, invoices, customers, db=None):
        self.invoices = invoices
        self.customers = customers
        self._db = db

    def close(self):
        if self._db is not None:
            self._db.close()

def get_repos() -> RepoContainer:
    if settings.use_sql_repos:
        db = SessionLocal()
        return RepoContainer(
            invoices=InvoiceRepoSQL(db),
            customers=CustomerRepoSQL(db),
            db=db,
        )
    else:
        return RepoContainer(
            invoices=InvoiceRepoMemory(),
            customers=CustomerRepoMemory(),
        )
