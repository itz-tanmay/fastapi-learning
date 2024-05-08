"""create content in post table

Revision ID: a402c00f421e
Revises: b5e6bb6b8c8d
Create Date: 2024-05-07 16:25:29.783366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a402c00f421e'
down_revision: Union[str, None] = 'b5e6bb6b8c8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
