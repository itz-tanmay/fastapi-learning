"""create post table

Revision ID: b5e6bb6b8c8d
Revises: 
Create Date: 2024-05-07 16:20:47.491466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5e6bb6b8c8d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts",
                    sa.Column("id", sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column("title", sa.String(),
                              nullable=False),
                    )


def downgrade() -> None:
    op.drop_table("posts")
