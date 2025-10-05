"""merge heads

Revision ID: 181e344b6d4c
Revises: e56de1e85916, 8c4d247ad1a4
Create Date: 2025-10-05 16:19:54.102247

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "181e344b6d4c"
down_revision: Union[str, None] = ("e56de1e85916", "8c4d247ad1a4")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
