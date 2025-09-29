# backend/alembic/versions/06697752218d_sync_invoices_table_columns.py

from alembic import op
import sqlalchemy as sa

# --- Alembic identifiers ---
revision = "06697752218d"  # must match filename prefix
down_revision = None  # make this the base of your history
branch_labels = None
depends_on = None


def upgrade():
    # add invoices.tax_total if it doesn't exist (idempotent)
    bind = op.get_bind()
    insp = sa.inspect(bind)

    if "invoices" in insp.get_table_names():
        cols = {c["name"] for c in insp.get_columns("invoices")}
        if "tax_total" not in cols:
            op.add_column(
                "invoices",
                sa.Column("tax_total", sa.Numeric(12, 2), nullable=False, server_default="0"),
            )
            # drop the default after backfill
            op.alter_column("invoices", "tax_total", server_default=None)


def downgrade():
    bind = op.get_bind()
    insp = sa.inspect(bind)
    if "invoices" in insp.get_table_names():
        cols = {c["name"] for c in insp.get_columns("invoices")}
        if "tax_total" in cols:
            op.drop_column("invoices", "tax_total")
