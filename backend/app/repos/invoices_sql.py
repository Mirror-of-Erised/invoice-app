# backend/app/repos/invoices_sql.py
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal
from uuid import UUID

from app.models.invoice import Invoice
from app.models.invoice_line_item import InvoiceLineItem
from app.models.organization import Organization
from app.schemas.invoice import InvoiceCreate


class InvoiceRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit=100, offset=0):
        return self.db.query(Invoice).offset(offset).limit(limit).all()

    def get(self, invoice_id: UUID):
        return self.db.get(Invoice, invoice_id)

    def create(self, data: InvoiceCreate):
        payload = data.model_dump()
        org_id = payload.get("organization_id")

        if org_id is None:
            # fallback: use the first organization in DB
            org = self.db.query(Organization).order_by(Organization.created_at.asc()).first()
            if not org:
                raise ValueError("No organization found; seed an organization first.")
            org_id = org.id

        inv = Invoice(
            number=payload["number"],
            customer_id=payload["customer_id"],
            organization_id=org_id,
            issue_date=date.today(),
            status="draft",
            currency="USD",
            subtotal=Decimal("0.00"),
            tax=Decimal("0.00"),
            total=Decimal(str(payload.get("total") or 0)),
            created_at=date.today(),
            updated_at=date.today(),
        )
        self.db.add(inv)
        self.db.commit()
        self.db.refresh(inv)
        return inv

    # ----- line items -----
    def add_line_item(self, invoice_id: UUID, description: str, qty: float, unit_price: float):
        inv = self.get(invoice_id)
        if not inv:
            return None

        item_total = Decimal(str(qty)) * Decimal(str(unit_price))
        item = InvoiceLineItem(
            invoice_id=invoice_id,
            description=description,
            qty=Decimal(str(qty)),
            unit_price=Decimal(str(unit_price)),
            total=item_total,
        )
        self.db.add(item)

        # recompute totals
        self.db.flush()
        self._recalc_totals(inv)
        self.db.commit()
        self.db.refresh(item)
        self.db.refresh(inv)
        return item

    def list_line_items(self, invoice_id: UUID):
        return (
            self.db.query(InvoiceLineItem)
            .filter(InvoiceLineItem.invoice_id == invoice_id)
            .order_by(
                InvoiceLineItem.created_at.asc() if hasattr(InvoiceLineItem, "created_at") else InvoiceLineItem.id.asc()
            )
            .all()
        )

    def _recalc_totals(self, inv: Invoice):
        subtotal = Decimal("0.00")
        for li in inv.line_items:
            subtotal += Decimal(li.total)
        inv.subtotal = subtotal
        inv.tax = Decimal("0.00")  # placeholder; add tax logic later
        inv.total = inv.subtotal + inv.tax
        inv.updated_at = date.today()
