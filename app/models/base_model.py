from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field


class UUIDPrimaryKeyMixin(SQLModel):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )


class UserInfoMixin(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    username: str = Field(min_length=4, max_length=10, unique=True, index=True)
    email: str = Field(unique=True, index=True)
    phone_number: str
    avatar: bytes | None = None
    gender: str | None = None
    date_of_birth: str | None = None
    national_id_no: str | None = None
    is_active: bool = False
    is_verified: bool = False
    password_hash: str


class LoginInfoMixin(SQLModel):
    last_login: datetime = Field()
    failed_login_attempt: int = 0


class SoftDeleteMixin(SQLModel):
    is_deleted: bool = False
    deleted_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )


