from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, DateTime, func

from app.models.base_model import UUIDPrimaryKeyMixin, UserInfoMixin, SoftDeleteMixin

from sqlmodel import SQLModel, Field, Relationship


class Address(UUIDPrimaryKeyMixin, SQLModel):
    street: str
    city: str
    state: str
    country: str
    zip_postal_code: str | None = Field(default=None, min_length=6, max_length=6)
    latitude: float | None = None
    longitude: float | None = None


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


class User(UUIDPrimaryKeyMixin, UserInfoMixin, SoftDeleteMixin, SQLModel, table=True):
    login_timelines: list["LoginEventInfo"] = Relationship(back_populates="user", cascade_delete=True)

    update_events: list["UserEventUpdate"] = Relationship(back_populates="user", cascade_delete=True)



class LoginEventInfo(SQLModel, table=True):
    _last_login: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )
    _failed_login_attempt: int = 0

    user_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    user: "User" = Relationship(back_populates="login_timelines")


class UserEventUpdate(SQLModel, table=True):
    first_name: str | None = None
    last_name: str | None = None
    email: str = Field(primary_key=True,unique=True)
    _phone_number: str
    avatar: bytes | None = None
    _password_hash: str

    user_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    user: "User" = Relationship(back_populates="update_events")