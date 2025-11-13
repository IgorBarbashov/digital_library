"""insert genres

Revision ID: c912e2fca348
Revises: fb90f8f0e96a
Create Date: 2025-11-13 14:27:35.781572

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c912e2fca348"
down_revision: Union[str, Sequence[str], None] = "fb90f8f0e96a"
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

    genre_table = sa.table("genre", sa.column("name", sa.String))
    op.bulk_insert(genre_table, [{"name": genre} for genre in genres])


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "DELETE FROM genre WHERE name IN ("
        "'Фэнтези', 'Научная фантастика', 'Детектив', 'Триллер', "
        "'Любовный роман', 'Приключения', 'Ужасы', 'Антиутопия', "
        "'Историческая литература', 'Юмор')"
    )
