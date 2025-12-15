"""created user schema

Revision ID: 002ddb92b475
Revises: 
Create Date: 2025-12-15 09:56:12.036496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002ddb92b475'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key = True),
        sa.Column("username", sa.String(20), nullable=False),
        sa.Column("email", sa.String(30), unique=True, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user")
