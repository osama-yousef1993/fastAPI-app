"""create_tables

Revision ID: b1fbfb201ed2
Revises:
Create Date: 2024-04-18 23:47:32.637698

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b1fbfb201ed2"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("first_name", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("last_name", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("email", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("password", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("profiles", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column(
            "is_admin",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "is_verified",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "otp",
            sa.INTEGER(),
            server_default=sa.text("0"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "otp_expiration_time",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "deleted_at",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
        sa.UniqueConstraint("email", name="users_email_key"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("users_last_name_idx", "users", ["last_name"], unique=False)
    op.create_index("users_id_idx1", "users", ["id"], unique=False)
    op.create_index("users_id_idx", "users", ["id"], unique=False)
    op.create_index("users_first_name_idx", "users", ["first_name"], unique=False)
    op.create_index("users_email_idx", "users", ["email"], unique=False)
    op.create_table(
        "tracking",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("user_id", sa.UUID(), autoincrement=False, nullable=True),
        sa.Column("image_input", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("image_output", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("service_type", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("credits", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "response_time",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("status_code", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("response", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="tracking_user_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="tracking_pkey"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tracking")
    op.drop_index("users_email_idx", table_name="users")
    op.drop_index("users_first_name_idx", table_name="users")
    op.drop_index("users_id_idx", table_name="users")
    op.drop_index("users_id_idx1", table_name="users")
    op.drop_index("users_last_name_idx", table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
