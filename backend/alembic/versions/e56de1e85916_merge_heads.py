"""merge heads

Revision ID: e56de1e85916
Revises: 06697752218d, 7017859f91e0
Create Date: 2025-10-05 16:00:15.972917

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "e56de1e85916"
down_revision: Union[str, None] = ("06697752218d", "7017859f91e0")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
