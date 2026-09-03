from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field
import sqlalchemy as sa

from app.security.schema.auth import AuthSessionStatus


class AuthSession(SQLModel, table=True):
    __tablename__ = "auth_session"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    user_id: UUID = Field(
        foreign_key="user.id",
        index=True,
        nullable=False
    )

    family_token_id: UUID = Field(
        unique=True,
        index=True
    )

    status: AuthSessionStatus = Field(
        default=AuthSessionStatus.ACTIVE,
        index=True,
        nullable=False
    )

    created_at: datetime = Field(
        default_factory=lambda : datetime.now(tz=timezone.utc),
        sa_type=sa.DateTime(timezone=True), #type: ignore
        nullable=False
    )

    expires_at: datetime = Field(
        sa_type=sa.DateTime(timezone=True), #type: ignore
        nullable=False,
        index=True
    )

    last_used_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True), #type: ignore
    )

    revoked_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True), #type: ignore
    )

    revoked_reason: str | None = Field(
        default=None
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