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

issue = date.today()
due = issue + timedelta(days=30)
inv_num = "INV-1001"


def get_invoice_number_column(conn) -> str:
    """Return 'invoice_number' or 'number' depending on schema."""
    col = conn.execute(
        text(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'invoices'
              AND column_name IN ('invoice_number', 'number')
            ORDER BY CASE column_name WHEN 'invoice_number' THEN 0 ELSE 1 END
            LIMIT 1
        """
        )
    ).scalar()
    if not col:
        raise RuntimeError("No invoice number column found on invoices (expected 'invoice_number' or 'number').")
    return col


def has_unique_on_org_and_num(conn, num_col: str) -> bool:
    """Return True if there is a UNIQUE constraint/index on (organization_id, <num_col>)."""
    rows = conn.execute(
        text(
            """
            SELECT c.conname,
                   ARRAY(
                     SELECT a.attname
                     FROM unnest(c.conkey) AS k(attnum)
                     JOIN pg_attribute a
                       ON a.attrelid = c.conrelid AND a.attnum = k.attnum
                     ORDER BY a.attnum
                   ) AS cols
            FROM pg_constraint c
            JOIN pg_class t ON t.oid = c.conrelid
            JOIN pg_namespace n ON n.oid = t.relnamespace
            WHERE c.contype = 'u'
              AND t.relname = 'invoices'
        """
        )
    ).all()

    target = {"organization_id", num_col}
    for _, cols in rows:
        if set(cols) == target:
            return True
    return False


with engine.begin() as conn:
    # --- Organization (upsert by unique name) ---
    org_id = conn.execute(
        text(
            """
        INSERT INTO organizations (name)
        VALUES ('Demo Org')
        ON CONFLICT (name) DO UPDATE
          SET name = EXCLUDED.name
        RETURNING id
    """
        )
    ).scalar_one()

    # --- Customer (insert or get existing by (org, name)) ---
    cust_id = conn.execute(
        text(
            """
            WITH ins AS (
              INSERT INTO customers (organization_id, name, email)
              VALUES (:org, 'Acme, Inc.', 'billing@acme.test')
              ON CONFLICT DO NOTHING
              RETURNING id
            )
            SELECT id FROM ins
            UNION ALL
            SELECT id
            FROM customers
            WHERE organization_id = :org AND name = 'Acme, Inc.'
            LIMIT 1
        """
        ),
        {"org": org_id},
    ).scalar_one()

    # --- Figure out invoice number column + whether a unique exists ---
    num_col = get_invoice_number_column(conn)
    has_unique = has_unique_on_org_and_num(conn, num_col)

    # Build the insert list dynamically so we set both if both exist
    # (covers mixed schemas with 'number' and 'invoice_number')
    number_cols = (
        conn.execute(
            text(
                """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'invoices'
              AND column_name IN ('invoice_number','number')
            ORDER BY column_name
        """
            )
        )
        .scalars()
        .all()
    )

    # Some installs have both tax_total and tax; set both if present.
    tax_cols = (
        conn.execute(
            text(
                """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'invoices'
              AND column_name IN ('tax_total','tax')
            ORDER BY column_name
        """
            )
        )
        .scalars()
        .all()
    )

    # Compose the column/value lists
    base_cols = [
        "organization_id",
        "customer_id",
        "status",
        "issue_date",
        "due_date",
        "currency",
        "subtotal",
        "total",
        "notes",
    ]
    base_vals = [":org", ":cust", "'sent'", ":issue", ":due", "'USD'", "1550.00", "1550.00", "'Demo invoice'"]

    # Add number columns
    for c in number_cols:
        base_cols.insert(2, c)  # keep them near the top
        base_vals.insert(2, ":num")

    # Add tax columns (set zeros)
    for c in tax_cols:
        # place before total/notes to be tidy; not required but readable
        insert_pos = base_cols.index("total")
        base_cols.insert(insert_pos, c)
        base_vals.insert(insert_pos, "0.00")

    columns_sql = ", ".join(base_cols)
    values_sql = ", ".join(base_vals)

    if has_unique:
        # Use ON CONFLICT (organization_id, <num_col>)
        inv_id = conn.execute(
            text(
                f"""
                INSERT INTO invoices
                  ({columns_sql})
                VALUES
                  ({values_sql})
                ON CONFLICT (organization_id, {num_col})
                DO UPDATE SET
                  notes = EXCLUDED.notes
                RETURNING id
            """
            ),
            {"org": org_id, "cust": cust_id, "num": inv_num, "issue": issue, "due": due},
        ).scalar_one()
    else:
        # No unique pair — do idempotent select then insert
        inv_id = conn.execute(
            text(
                f"""
                SELECT id
                FROM invoices
                WHERE organization_id = :org AND {num_col} = :num
                LIMIT 1
            """
            ),
            {"org": org_id, "num": inv_num},
        ).scalar()

        if not inv_id:
            inv_id = conn.execute(
                text(
                    f"""
                    INSERT INTO invoices
                      ({columns_sql})
                    VALUES
                      ({values_sql})
                    RETURNING id
                """
                ),
                {"org": org_id, "cust": cust_id, "num": inv_num, "issue": issue, "due": due},
            ).scalar_one()

    # --- Line items: keep seed idempotent (replace items for this invoice) ---
    conn.execute(text("DELETE FROM invoice_line_items WHERE invoice_id = :inv"), {"inv": inv_id})
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
