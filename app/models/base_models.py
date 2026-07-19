from datetime import datetime, date
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field

from app.enums.user_enums import GenderEnum


class UUIDPrimaryKeyMixin(SQLModel):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )


class UserInfoMixin(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    username: str = Field(min_length=4, max_length=30, unique=True, index=True)
    email: str = Field(unique=True, index=True)
    phone_number: str = Field(index=True)
    avatar_url: str | None = None
    gender: GenderEnum | None = None
    date_of_birth: date | None = None
    is_active: bool = Field(default=False, index=True)
    is_verified: bool = False
    password_hash: str
    last_login: datetime
    failed_login_attempt: int = 0


class SoftDeleteMixin(SQLModel):
    is_deleted: bool = Field(default=False, index=True)

    deleted_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )


class TimestampMixin(SQLModel):
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
            index=True
        )
    )

    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            onupdate=func.now(),
            nullable=False
        )
    )


class AuditMixin(SQLModel):
    created_by: UUID
    updated_by: UUID

