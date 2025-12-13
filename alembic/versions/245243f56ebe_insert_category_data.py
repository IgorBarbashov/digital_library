
import uuid
from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op


revision: str = "245243f56ebe"
down_revision: Union[str, Sequence[str], None] = "db2e9d067dd5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    categories = [
        "Художественная литература",
        "Научная литература",
        "Техническая литература",
        "Бизнес и экономика",
        "Учебная литература",
        "Детская литература",
        "Справочная литература",
        "Биографии и мемуары",
    ]

    category_table = sa.table(
        "category",
        sa.column("id", UUID(as_uuid=True)),
        sa.column("create_at", sa.DateTime),
        sa.column("update_at", sa.DateTime),
        sa.column("name", sa.String),
    )

    now = datetime.utcnow()

    op.bulk_insert(
        category_table,
        [
            {
                "id": str(uuid.uuid4()),
                "create_at": now,
                "update_at": now,
                "name": category,
            }
            for category in categories
        ],
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM category WHERE name IN ("
        "'Художественная литература', 'Научная литература', "
        "'Техническая литература', 'Бизнес и экономика', "
        "'Учебная литература', 'Детская литература', "
        "'Справочная литература', 'Биографии и мемуары')"
    )
