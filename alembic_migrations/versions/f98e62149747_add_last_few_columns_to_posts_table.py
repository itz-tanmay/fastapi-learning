"""add last few columns to posts table

Revision ID: f98e62149747
Revises: 75eb27adef3e
Create Date: 2024-05-07 16:59:20.827238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f98e62149747'
down_revision: Union[str, None] = '75eb27adef3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column("posts",
                  sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")), )


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
