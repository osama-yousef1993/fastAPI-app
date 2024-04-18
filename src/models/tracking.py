from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID

from src.database.database import default_now, metaData, new_uuid, now

tracking = Table(
    "tracking",
    metaData,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=new_uuid,
        index=True,
    ),
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", name="fk_tracking_users"),
        nullable=False,
    ),
    Column("image", String, nullable=False),
    Column("image_input", String, nullable=False),
    Column("image_output", String, nullable=False),
    Column("service_type", String, nullable=False),
    Column("response", String, nullable=False),
    Column("status_code", Integer, nullable=False),
    Column("credits", Integer, nullable=False),
    Column("response_time", DateTime, nullable=False, onupdate=now, **default_now),
    Column("created_at", DateTime, nullable=False, onupdate=now, **default_now),
)
