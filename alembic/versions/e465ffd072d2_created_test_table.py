"""created test table

Revision ID: e465ffd072d2
Revises: fca608aa76d2
Create Date: 2025-12-15 11:08:55.842999

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e465ffd072d2'
down_revision: Union[str, Sequence[str], None] = 'fca608aa76d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "test",
        sa.Column("name",sa.String(50),nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("test")
