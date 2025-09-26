# backend/app/repositories/memory/customer_repo.py
from typing import List, Dict, Any


class CustomerRepoMemory:
    def __init__(self):
        self._rows: List[Dict[str, Any]] = []

    def add(self, name: str, email: str | None = None):
        self._rows.append({"name": name, "email": email})
