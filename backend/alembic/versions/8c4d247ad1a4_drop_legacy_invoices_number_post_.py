from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = "8c4d247ad1a4"  # leave as generated
down_revision = "7017859f91e0"  # your backfill revision id
branch_labels = None
depends_on = None


def upgrade():

    # 1) Drop any constraint or index tied to legacy `number` (defensive)
    #    (Constraint-by-name guard; ignore if not present)
    op.execute(
        text(
            """
    DO $$
    BEGIN
        IF EXISTS (
            SELECT 1 FROM pg_constraint
            WHERE conrelid = 'invoices'::regclass
              AND conname  = 'uq_invoices_number'
        ) THEN
            ALTER TABLE invoices DROP CONSTRAINT uq_invoices_number;
        END IF;
    END$$;
    """
        )
    )

    # 2) Drop any indexes on `number` (common legacy names guarded)
    for idx in ("ix_invoices_number", "invoices_number_idx", "uq_invoices_number_idx"):
        op.execute(
            text(
                f"""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM pg_indexes
                WHERE schemaname = 'public' AND tablename = 'invoices' AND indexname = '{idx}'
            ) THEN
                DROP INDEX IF EXISTS {idx};
            END IF;
        END$$;
        """
            )
        )

    # 3) Finally drop the column if it still exists
    op.execute(
        text(
            """
    DO $$
    BEGIN
        IF EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name='invoices' AND column_name='number'
        ) THEN
            ALTER TABLE invoices DROP COLUMN number;
        END IF;
    END$$;
    """
        )
    )


def downgrade():
    # Recreate the legacy column as nullable (no indexes/constraints)
    op.add_column("invoices", sa.Column("number", sa.String(length=50), nullable=True))
