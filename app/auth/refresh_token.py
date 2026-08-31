from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field
import sqlalchemy as sa


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: UUID = Field(
        primary_key=True
    )

    user_id: UUID = Field(
        foreign_key="user.id",
        nullable=False,
        index=True
    )

    session_id: UUID = Field(
        foreign_key="auth_session.id",
        index=True,
        nullable=True
    )

    token_family_id: UUID = Field(
        index=True,
        nullable=False
    )

    token_hash: str = Field(
        unique=True,
        index=True,
        nullable=False
    )

    issued_at: datetime = Field(
        default_factory=lambda : datetime.now(tz=timezone.utc),
        sa_type=sa.DateTime(timezone=True), #type:ignore
        nullable=False
    )

    expires_at: datetime = Field(
        nullable=False,
        sa_type=sa.DateTime(timezone=True), #type:ignore
        index=True
    )

    used_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True), #type:ignore
    )

    revoked_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True), #type:ignore
    )

    replaced_by_token_id: UUID | None = Field(
        default=None
    )
