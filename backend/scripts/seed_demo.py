from __future__ import annotations
import os
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load repo-root .env (invoice-app/.env)
ROOT = Path(__file__).resolve().parents[3]
load_dotenv(ROOT / ".env")

engine = create_engine(os.environ["DATABASE_URL"], future=True)

with engine.begin() as conn:
    # org
    org_id = conn.execute(text("INSERT INTO organizations (name) VALUES ('Demo Org') RETURNING id")).scalar_one()

    # customer
    cust_id = conn.execute(
        text(
            """
            INSERT INTO customers (organization_id, name, email)
            VALUES (:org, 'Acme, Inc.', 'billing@acme.test')
            RETURNING id
        """
        ),
        {"org": org_id},
    ).scalar_one()

    # invoice
    inv_id = conn.execute(
        text(
            """
            INSERT INTO invoices
              (organization_id, customer_id, invoice_number, status, issue_date, due_date,
               currency, subtotal, tax, total, notes)
            VALUES
              (:org, :cust, 'INV-1001', 'sent', :issue, :due, 'USD', 1550.00, 0.00, 1550.00, 'Demo invoice')
            RETURNING id
        """
        ),
        {"org": org_id, "cust": cust_id, "issue": date.today(), "due": date.today() + timedelta(days=30)},
    ).scalar_one()

    # line items
    conn.execute(
        text(
            """
            INSERT INTO invoice_line_items
              (invoice_id, position, description, quantity, unit_price, line_total)
            VALUES
              (:inv, 1, 'Consulting', 10.00, 150.00, 1500.00),
              (:inv, 2, 'Hosting',     1.00,  50.00,   50.00)
        """
        ),
        {"inv": inv_id},
    )

print("seed_ok")
