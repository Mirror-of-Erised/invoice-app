from typing import Optional, Iterable

class InMemoryOrganizationRepo:
    def __init__(self):
        self._data: dict[int, dict] = {}
        self._by_name: dict[str, int] = {}
        self._seq = 1

    def create(self, name: str, email: str | None = None) -> dict:
        oid = self._seq; self._seq += 1
        org = {"id": oid, "name": name, "email": email}
        self._data[oid] = org
        self._by_name[name] = oid
        return org

    def get(self, org_id: int) -> Optional[dict]:
        return self._data.get(org_id)

    def by_name(self, name: str) -> Optional[dict]:
        oid = self._by_name.get(name)
        return self._data.get(oid) if oid else None

    def list(self) -> Iterable[dict]:
        return list(self._data.values())
