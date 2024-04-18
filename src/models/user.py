from sqlalchemy import Boolean, Column, DateTime, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID

from src.database.database import default_now, metaData, new_uuid, now

users = Table(
    "users",
    metaData,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=new_uuid,
        index=True,
    ),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("email", String, nullable=False, unique=True),
    Column("password", String, nullable=False),
    Column("profiles", String, nullable=False),
    Column("is_admin", Boolean, nullable=False),
    Column("is_verified", Boolean, nullable=False, default=False),
    Column("otp", Integer, nullable=False, default=False),
    Column("otp_expiration_time", DateTime(timezone=True), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, **default_now),
    Column("deleted_at", DateTime(timezone=True), nullable=True),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        onupdate=now,
        **default_now,
    ),
)
