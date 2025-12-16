"""created user schema

Revision ID: ae76c0e0e44a
Revises: 
Create Date: 2025-12-11 14:21:17.286281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae76c0e0e44a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(100), nullable = False),
        sa.Column("email", sa.String(50), nullable=False, unique=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user")
