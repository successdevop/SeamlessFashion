from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, DateTime, func

from app.enums.user_enums import UserRoleEnum, AddressTypeEnum
from app.models.base_model import UUIDPrimaryKeyMixin, UserInfoMixin, SoftDeleteMixin, TimestampMixin

from sqlmodel import SQLModel, Field, Relationship


class IdentityVerification(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    national_identification_no: str
    bank_verification_no: str | None = None

    user_id: UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="national_id_no")


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


class Address(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
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

    assigned_by: UUID
    assigned_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )

    user: "User" = Relationship(back_populates="roles")
    role: "Role" = Relationship(back_populates="users")


class RolePermission(TimestampMixin, SQLModel, table=True):
    role_id: UUID = Field(
        foreign_key="role.id",
        primary_key=True
    )

    permission_id: UUID = Field(
        foreign_key="permission.id",
        primary_key=True
    )


class Role(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: UserRoleEnum
    description: str | None = None
    is_system: bool = False

    # a single role can have many users assigned to it(User-Role relationship)
    users: list[UserRole] = Relationship(back_populates="role")

    # a single role can have many permissions assigned to it to perform (Role-Permission relationship)
    permissions: list["Permission"] = Relationship(back_populates="roles", link_model=RolePermission)


class Permission(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str
    resource: str
    action: str
    description: str | None = None

    # a permission can have many roles performing it(Role-Permission relationship)
    roles: list["Role"] = Relationship(back_populates="permissions", link_model=RolePermission)


class User(UUIDPrimaryKeyMixin, UserInfoMixin, TimestampMixin, SoftDeleteMixin, SQLModel, table=True):

    national_id_no: IdentityVerification = Relationship(back_populates="user")

    # a user can perform many roles/have many roles assigned to it(User-Role relationship)
    roles: list[UserRole] = Relationship(back_populates="user")

    # a user can have more than one address(User-Address relationship)
    address: list[UserAddress] = Relationship(back_populates="user")

    # keeps record of all login information
    login_timelines: list["LoginEventInfo"] = Relationship(back_populates="user")

    # keeps record of all user profile updates
    update_events: list["User"]


class LoginEventInfo(UUIDPrimaryKeyMixin, SQLModel, table=True):
    login_time: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )
    ip_address: str
    device: str
    browser: str
    location: str
    successful: bool = False

    user_id: UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="login_timelines")
