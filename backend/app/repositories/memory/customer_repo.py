from typing import Optional, Iterable

class InMemoryCustomerRepo:
    def __init__(self):
        self._data: dict[int, dict] = {}
        self._by_org: dict[int, list[int]] = {}
        self._seq = 1

    def create(self, organization_id: int, name: str, email: str | None = None,
               phone: str | None = None, billing_address: str | None = None) -> dict:
        cid = self._seq; self._seq += 1
        c = {
            "id": cid,
            "organization_id": organization_id,
            "name": name,
            "email": email,
            "phone": phone,
            "billing_address": billing_address,
        }
        self._data[cid] = c
        self._by_org.setdefault(organization_id, []).append(cid)
        return c

    def get(self, customer_id: int) -> Optional[dict]:
        return self._data.get(customer_id)

    def list_by_org(self, organization_id: int) -> Iterable[dict]:
        ids = self._by_org.get(organization_id, [])
        return [self._data[i] for i in ids]
