from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field
import sqlalchemy as sa


class SecurityAudit(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    user_id: UUID = Field(
        foreign_key="user.id",
        index=True,
        nullable=False
    )

    event_type: str = Field(
        index=True,
        nullable=False
    )

    session_id: UUID = Field(
        foreign_key="auth_session.id",
        index=True,
        nullable=False
    )

    token_family_id: UUID = Field(
        nullable=False
    )

    occurred_at: datetime = Field(
        nullable=False,
        sa_type=sa.DateTime(timezone=True), #type:ignore
        index=True
    )

    device_name: str | None = Field(
        default=None
    )

    user_agent: str | None = Field(
        default=None
    )

    ip_address: str | None = Field(
        default=None
    )
