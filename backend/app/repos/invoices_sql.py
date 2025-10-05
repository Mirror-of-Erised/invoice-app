# backend/app/repos/invoices_sql.py
from sqlalchemy.orm import Session
from datetime import date, timedelta
from decimal import Decimal
from uuid import UUID

from app.models.invoice import Invoice
from app.models.invoice_line_item import InvoiceLineItem
from app.models.organization import Organization
from app.schemas.invoice import InvoiceCreate


class InvoiceRepo:
    def __init__(self, db: Session):
        self.db = db

    # ---------- internal helpers ----------
    def _ensure_canonical(self, inv: Invoice) -> Invoice:
        """
        Legacy fallback no longer required since `number` column was dropped.
        Kept for interface stability.
        """
        return inv

    # ---------- invoices ----------
    def list(self, limit=100, offset=0):
        objs = self.db.query(Invoice).offset(offset).limit(limit).all()
        return [self._ensure_canonical(o) for o in objs]

    def get(self, invoice_id: UUID):
        obj = self.db.get(Invoice, invoice_id)
        return self._ensure_canonical(obj)

    def create(self, data: InvoiceCreate):
        payload = data.model_dump()
        org_id = payload.get("organization_id")

        if org_id is None:
            # No created_at on Organization; pick a deterministic default (first by id).
            org = self.db.query(Organization).order_by(Organization.id.asc()).first()
            if not org:
                raise ValueError("No organization found; seed an organization first.")
            org_id = org.id

        # ---- required defaults (match NOT NULLs in DB) ----
        issue = payload.get("issue_date") or date.today()
        due = payload.get("due_date") or (issue + timedelta(days=30))
        status = payload.get("status") or "draft"

        # Money fields: keep Decimal-friendly, fall back sanely
        total = Decimal(str(payload.get("total", "0.00")))
        subtotal = Decimal(str(payload.get("subtotal", total)))
        tax_total = Decimal(str(payload.get("tax_total", "0.00")))

        inv = Invoice(
            organization_id=org_id,
            customer_id=payload["customer_id"],
            invoice_number=payload["invoice_number"],  # canonical
            issue_date=issue,
            due_date=due,
            status=status,
            subtotal=subtotal,
            tax_total=tax_total,
            total=total,
        )
        self.db.add(inv)
        self.db.commit()
        self.db.refresh(inv)
        return self._ensure_canonical(inv)

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
            subtotal += Decimal(str(li.total))
        inv.subtotal = subtotal
        # keep tax simple for now; adjust when tax rules exist
        inv.tax_total = Decimal("0.00")
        inv.total = inv.subtotal + inv.tax_total
        # If updated_at exists and is Date/DateTime, set something reasonable
        if hasattr(inv, "updated_at"):
            try:
                inv.updated_at = date.today()
            except Exception:
                # silently ignore if it's a DateTime and you prefer utcnow in your model
                pass
