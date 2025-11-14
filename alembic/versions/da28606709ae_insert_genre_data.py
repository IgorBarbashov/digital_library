"""Insert Genre data

Revision ID: da28606709ae
Revises: 843cc651aad2
Create Date: 2025-11-14 12:51:22.178804

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "da28606709ae"
down_revision: Union[str, Sequence[str], None] = "843cc651aad2"
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
