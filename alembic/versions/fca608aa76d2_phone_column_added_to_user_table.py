"""phone column added to user table

Revision ID: fca608aa76d2
Revises: 002ddb92b475
Create Date: 2025-12-15 10:46:53.517696

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fca608aa76d2'
down_revision: Union[str, Sequence[str], None] = '002ddb92b475'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "user",
        sa.Column("phone", sa.String(10), unique=True, nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user","phone")
