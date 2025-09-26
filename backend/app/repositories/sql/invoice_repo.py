from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session


class InvoiceRepoSQL:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_invoice_summaries(self):
        return self.db.execute(text("SELECT invoice_number, total FROM invoices ORDER BY invoice_number")).all()
