from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, DateTime, func

from app.enums.user_enums import UserRoleEnum, AddressTypeEnum
from app.models.base_model import UUIDPrimaryKeyMixin, UserInfoMixin, SoftDeleteMixin

from sqlmodel import SQLModel, Field, Relationship


class UserAddress(SQLModel, table=True):
    user_id: UUID = Field(
        foreign_key="user.id",
        primary_key=True
    )

    address_id: UUID = Field(
        foreign_key="address.id",
        primary_key=True
    )

    address_type: AddressTypeEnum
    is_default: bool = False

    user: "User" = Relationship(back_populates="address")
    address: "Address" = Relationship(back_populates="user")


class Address(UUIDPrimaryKeyMixin, SQLModel, table=True):
    street: str
    city: str
    state: str
    country: str
    zip_postal_code: str | None = Field(default=None, min_length=6, max_length=6)
    latitude: float | None = None
    longitude: float | None = None

    # an address can have multiple users(User-Address relationship)
    user: list[UserAddress] = Relationship(back_populates="address")


class UserRole(SQLModel, table=True):
    user_id: UUID = Field(
        foreign_key="user.id",
        primary_key=True
    )

    role_id: UUID = Field(
        foreign_key="role.id",
        primary_key=True
    )

    assigned_by: "user.id"
    assigned_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )

    user: "User" = Relationship(back_populates="roles")
    role: "Role" = Relationship(back_populates="users")


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


class Role(UUIDPrimaryKeyMixin, SQLModel, table=True):
    name: UserRoleEnum
    description: str | None = None
    is_system: bool = False

    # a single role can have many users assigned to it(User-Role relationship)
    users: list[UserRole] = Relationship(back_populates="role")

    # a single role can have many permissions assigned to it to perform (Role-Permission relationship)
    permissions: list["Permission"] = Relationship(back_populates="roles", link_model=RolePermission)


class Permission(UUIDPrimaryKeyMixin, SQLModel, table=True):
    name: str
    resource: str
    action: str
    description: str | None = None

    # a permission can have many roles performing it(Role-Permission relationship)
    roles: list["Role"] = Relationship(back_populates="permissions", link_model=RolePermission)


class User(UUIDPrimaryKeyMixin, UserInfoMixin, SoftDeleteMixin, SQLModel, table=True):
    # a user can perform many roles/have many roles assigned to it(User-Role relationship)
    roles: list[UserRole] = Relationship(back_populates="user")

    # a user can have more than one address(User-Address relationship)
    address: list[UserAddress] = Relationship(back_populates="user")

    # keeps record of all login information
    login_timelines: list["LoginEventInfo"] = Relationship(back_populates="user", cascade_delete=True)

    # keeps record of all user profile updates
    update_events: list["UserEventUpdate"] = Relationship(back_populates="user", cascade_delete=True)


class LoginEventInfo(SQLModel, table=True):
    last_login: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )
    failed_login_attempt: int = 0

    user_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    user: "User" = Relationship(back_populates="login_timelines")


class UserEventUpdate(SQLModel, table=True):
    first_name: str | None = None
    last_name: str | None = None
    email: str = Field(primary_key=True,unique=True)
    phone_number: str
    avatar_url: str | None = None
    password_hash: str

    user_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    user: "User" = Relationship(back_populates="update_events")