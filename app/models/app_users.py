from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, DateTime, func

from app.models.base_model import UUIDPrimaryKeyMixin, UserInfoMixin, LoginInfoMixin, SoftDeleteMixin

from sqlmodel import SQLModel, Field


class Address(UUIDPrimaryKeyMixin, SQLModel):
    street: str
    city: str
    state: str
    country: str
    zip_postal_code: str = Field(ge=6, le=6)
    latitude: str
    longitude: str


class UserAddress(SQLModel, table=True):
    user_id: UUID = Field(
        foreign_key="user.id",
        primary_key=True
    )

    address_id: UUID = Field(
        foreign_key="address.id",
        primary_key=True
    )

    address_type: str
    is_default: str


class Role(UUIDPrimaryKeyMixin, SQLModel, table=True):
    name_of_role: str
    description: str | None = None
    is_system: bool = False


class Permission(UUIDPrimaryKeyMixin, SQLModel, table=True):
    name_of_permission: str
    resource: str
    action: str
    description: str | None = None


class UserRole(SQLModel, table=True):
    user_id: UUID = Field(
        foreign_key="user.id",
        primary_key=True
    )

    role_id: UUID = Field(
        foreign_key="role.id",
        primary_key=True
    )

    assigned_by: None
    assigned_at: None


class RolePermission(SQLModel, table=True):
    role_id: UUID = Field(
        foreign_key="role.id",
        primary_key=True
    )

    permission_id: UUID = Field(
        foreign_key="permission.id",
        primary_key=True
    )

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )


class User(UUIDPrimaryKeyMixin, UserInfoMixin, LoginInfoMixin, SoftDeleteMixin, SQLModel, table=True):
    pass

