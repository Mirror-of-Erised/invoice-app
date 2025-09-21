import uuid

from app.db.session import get_session
from app.models.organization import Organization

with get_session() as s:
    name = "Acme Org"
    org = s.query(Organization).filter(Organization.name == name).first()
    if not org:
        org = Organization(id=uuid.uuid4(), name=name)
        s.add(org)
        s.flush()
        print("Created org:", org.id)
    else:
        print("Org exists:", org.id)
