from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field


class UUIDPrimaryKeyMixin(SQLModel):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    _created_at: datetime = Field(
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
    _phone_number: str
    avatar: bytes | None = None
    _gender: str | None = None
    _date_of_birth: str | None = None
    _national_id_no: str | None = None
    _is_active: bool = False
    _is_verified: bool = False
    _password_hash: str


class SoftDeleteMixin(SQLModel):
    _is_deleted: bool = False
    _deleted_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )


