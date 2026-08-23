from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field

from app.enums.user_enums import OutboxStatus
from base_models.base_models import UUIDPrimaryKeyMixin


class OutBoxMessage(UUIDPrimaryKeyMixin, SQLModel, table=True):
    __tablename__ = "outbox_message"

    event_type: str = Field(
        index=True,
        nullable=False
    )
    payload: dict[str, Any] = Field(
        sa_column=Column(
            JSON,
            nullable=False
        )
    )
    status: OutboxStatus = Field(
        default=OutboxStatus.PENDING,
        index=True,
        nullable=False
    )
    attempts: int = Field(
        default=0,
        nullable=False
    )
    available_at: datetime = Field(
        default_factory=lambda : datetime.now(tz=timezone.utc),
        index=True,
        nullable=False
    )
    created_at: datetime = Field(
        default_factory=lambda : datetime.now(tz=timezone.utc),
        index=True,
        nullable=False
    )
    processed_at: datetime | None= Field(
        default=None
    )
    last_error: str | None = Field(
        default=None
    )