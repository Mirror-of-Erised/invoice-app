**Decision:** Use `invoice_number` as the canonical invoice identifier everywhere (DB, API, schemas, code).
**Rationale:** Avoid confusion with legacy `number`; aligns with API semantics and uniqueness needs.
**Constraints:**
- DB: `(organization_id, invoice_number)` is unique and `invoice_number` is NOT NULL.
- Code: All create/read/update use `invoice_number` only.
- Migration: Backfill `invoice_number` from `number` where needed; later drop `number`.
