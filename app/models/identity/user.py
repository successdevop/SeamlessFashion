from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, DateTime, func

from sqlmodel import SQLModel, Field, Relationship

from app.enums.user_enums import AddressTypeEnum, VerificationEnum
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin, UserInfoMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.base_models.base_tables import Address
    from app.models.identity.role import Role
    from app.models.organization.organisation import OrganisationMember


class IdentityVerification(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    national_identification_no: str
    bank_verification_no: str | None = None
    verification_status: VerificationEnum
    verified_at: datetime
    verified_by: UUID = Field(foreign_key="user.id")
    document_type: str

    user_id: UUID | None = Field(default=None, foreign_key="user.id")
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


class User(UUIDPrimaryKeyMixin, UserInfoMixin, TimestampMixin, SoftDeleteMixin, SQLModel, table=True):

    national_id_no: IdentityVerification = Relationship(back_populates="user")

    # a user can perform many roles/have many roles assigned to it(User-Role relationship)
    roles: list[UserRole] = Relationship(back_populates="user")

    # a user can have more than one address(User-Address relationship)
    address: list[UserAddress] = Relationship(back_populates="user")

    # keeps record of all login information
    login_timelines: list["LoginEventInfo"] = Relationship(back_populates="user")

    # one user can belong to many organization(Organisation-User relationship)
    organisations: list["OrganisationMember"] = Relationship(back_populates="user")


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
    operating_system: str
    country: str
    city: str
    user_agent: str
    session_id: str
    successful: bool = False

    # loginEvent-User relationship
    user_id: UUID = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="login_timelines")
