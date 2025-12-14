"""add_description_to_book

Revision ID: f2a1d8c9e3b5
Revises: 245243f56ebe
Create Date: 2025-12-13 18:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f2a1d8c9e3b5'
down_revision: Union[str, Sequence[str], None] = '245243f56ebe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('book', sa.Column('description', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('book', 'description')
