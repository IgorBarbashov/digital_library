"""Insert Genre data

Revision ID: e35b81215d6e
Revises: da14d399f331
Create Date: 2025-11-15 10:16:45.637766

"""

import uuid
from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e35b81215d6e"
down_revision: Union[str, Sequence[str], None] = "da14d399f331"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    genres = [
        "Фэнтези",
        "Научная фантастика",
        "Детектив",
        "Триллер",
        "Любовный роман",
        "Приключения",
        "Ужасы",
        "Антиутопия",
        "Историческая литература",
        "Юмор",
    ]

    genre_table = sa.table(
        "genre",
        sa.column("id", UUID(as_uuid=True)),
        sa.column("create_at", sa.DateTime),
        sa.column("update_at", sa.DateTime),
        sa.column("name", sa.String),
    )

    now = datetime.utcnow()

    op.bulk_insert(
        genre_table,
        [
            {
                "id": str(uuid.uuid4()),
                "create_at": now,
                "update_at": now,
                "name": genre,
            }
            for genre in genres
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "DELETE FROM genre WHERE name IN ("
        "'Фэнтези', 'Научная фантастика', 'Детектив', 'Триллер', "
        "'Любовный роман', 'Приключения', 'Ужасы', 'Антиутопия', "
        "'Историческая литература', 'Юмор')"
    )
