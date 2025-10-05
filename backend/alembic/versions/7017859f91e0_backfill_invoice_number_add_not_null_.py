from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = "7017859f91e0"
down_revision = "0df4f2f85b18"  # <-- chain to the stub we just created
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # 1) Backfill invoice_number from legacy number where missing
    conn.execute(
        text(
            """
        UPDATE invoices
        SET invoice_number = number
        WHERE invoice_number IS NULL
    """
        )
    )

    # 2) De-duplicate (organization_id, invoice_number)
    dups = conn.execute(
        text(
            """
        WITH d AS (
            SELECT organization_id, invoice_number, COUNT(*) AS c
            FROM invoices
            WHERE invoice_number IS NOT NULL
            GROUP BY organization_id, invoice_number
            HAVING COUNT(*) > 1
        )
        SELECT d.organization_id, d.invoice_number
        FROM d
    """
        )
    ).fetchall()

    for org_id, inv_no in dups:
        rows = conn.execute(
            text(
                """
            SELECT id
            FROM invoices
            WHERE organization_id = :org AND invoice_number = :no
            ORDER BY id ASC
        """
            ),
            {"org": org_id, "no": inv_no},
        ).fetchall()

        for idx, (row_id,) in enumerate(rows, start=1):
            if idx == 1:
                continue
            suffix = f"-{idx}"
            candidate = f"{inv_no}{suffix}"
            if len(candidate) > 50:
                candidate = candidate[-50:]
            conn.execute(
                text(
                    """
                UPDATE invoices
                SET invoice_number = :new_no
                WHERE id = :id
            """
                ),
                {"new_no": candidate, "id": row_id},
            )

    # 3) Make NOT NULL (adjust length/type if different in your model)
    op.alter_column(
        "invoices",
        "invoice_number",
        existing_type=sa.String(length=50),
        nullable=False,
        existing_nullable=True,
    )

    # 4) Composite unique constraint

    op.execute(
        text(
            """
    DO $$
    DECLARE
        tgt_name text := 'uq_invoices_org_invoice_number';
        existing_constraint text;
        existing_index text;
    BEGIN
        -- Is there already a UNIQUE constraint with that name?
        SELECT conname
        INTO existing_constraint
        FROM pg_constraint
        WHERE conrelid = 'invoices'::regclass
        AND conname  = tgt_name
        AND contype  = 'u';

        IF existing_constraint IS NULL THEN
            -- Is there an index with that name already (name collision case)?
            SELECT indexname
            INTO existing_index
            FROM pg_indexes
            WHERE schemaname = 'public'
            AND tablename  = 'invoices'
            AND indexname  = tgt_name;

            IF existing_index IS NOT NULL THEN
                -- Convert the existing index into the table's UNIQUE constraint
                EXECUTE format(
                    'ALTER TABLE invoices ADD CONSTRAINT %I UNIQUE USING INDEX %I;',
                    tgt_name, tgt_name
                );
            ELSE
                -- Create the constraint fresh
                EXECUTE format(
                    'ALTER TABLE invoices ADD CONSTRAINT %I UNIQUE (organization_id, invoice_number);',
                    tgt_name
                );
            END IF;
        END IF;
    END$$;
    """
        )
    )


def downgrade():
    op.drop_constraint("uq_invoices_org_invoice_number", "invoices", type_="unique")
    op.alter_column(
        "invoices",
        "invoice_number",
        existing_type=sa.String(length=50),
        nullable=True,
        existing_nullable=False,
    )
