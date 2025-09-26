# backend/app/repositories/memory/invoice_repo.py
from typing import List, Dict, Any

class InvoiceRepoMemory:
    def __init__(self):
        self._rows: List[Dict[str, Any]] = []

    def list_invoice_summaries(self):
        return [(r["invoice_number"], r["total"]) for r in self._rows]

    def add(self, invoice_number: str, total: float):
        self._rows.append({"invoice_number": invoice_number, "total": total})
