"""Insert Role and User data

Revision ID: 51915c6a9eca
Revises: 30f3229dabd2
Create Date: 2025-11-21 12:59:32.572578

"""
import uuid
from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '51915c6a9eca'
down_revision: Union[str, Sequence[str], None] = '30f3229dabd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    roles = [
        "admin",
        "user",
    ]

    role_table = sa.table(
        "role",
        sa.column("id", UUID(as_uuid=True)),
        sa.column("create_at", sa.DateTime),
        sa.column("update_at", sa.DateTime),
        sa.column("name", sa.String),
    )

    now = datetime.utcnow()

    op.bulk_insert(
        role_table,
        [
            {
                "id": str(uuid.uuid4()),
                "create_at": now,
                "update_at": now,
                "name": role,
            }
            for role in roles
        ],
    )

    user_table = sa.table(
        "user",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.column("create_at", sa.DateTime),
        sa.column("update_at", sa.DateTime),
        sa.Column("username", sa.String(length=64), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("first_name", sa.String(length=64), nullable=False),
        sa.Column("last_name", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column(
            "disabled", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
        sa.Column("password_changed_at", sa.DateTime(), nullable=True, default=None),
        sa.Column(
            "failed_login_attempts", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column(
            "role_id",
            UUID(as_uuid=True),
            sa.ForeignKey("role.id", ondelete="RESTRICT"),
            nullable=False,
        ),
    )

    admin_role_uuid = (
        op.get_bind()
        .execute(sa.text("SELECT id FROM role WHERE name = 'admin'"))
        .scalar()
    )

    user_role_uuid = (
        op.get_bind()
        .execute(sa.text("SELECT id FROM role WHERE name = 'user'"))
        .scalar()
    )

    op.bulk_insert(
        user_table,
        [
            {
                "id": uuid.uuid4(),
                "create_at": now,
                "update_at": now,
                "username": "admin",
                "hashed_password": "hashed_admin_password",
                "first_name": "Admin",
                "last_name": "Admin",
                "email": "admin@example.com",
                "disabled": False,
                "password_changed_at": None,
                "failed_login_attempts": 0,
                "role_id": admin_role_uuid,
            },
            {
                "id": uuid.uuid4(),
                "create_at": now,
                "update_at": now,
                "username": "user",
                "hashed_password": "hashed_user_password",
                "first_name": "User",
                "last_name": "User",
                "email": "user@example.com",
                "disabled": False,
                "password_changed_at": None,
                "failed_login_attempts": 0,
                "role_id": user_role_uuid,
            },
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.get_bind().execute(
        sa.text("DELETE FROM user WHERE username IN ('admin', 'user')")
    )

    op.get_bind().execute(sa.text("DELETE FROM role WHERE name IN ('admin', 'user')"))

