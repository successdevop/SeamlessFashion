from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Column, DateTime, func, Index

from sqlmodel import SQLModel, Field, Relationship

from app.enums.user_enums import AddressTypeEnum
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin, UserInfoMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models import Address, IdentityVerification, OrganisationMember, RoleAssignment, Organisation


class UserAddress(SoftDeleteMixin, SQLModel, table=True):
    user_id: UUID = Field(
        foreign_key="user.id",
        primary_key=True
    )

    address_id: UUID = Field(
        foreign_key="address.id",
        primary_key=True
    )

    address_type: AddressTypeEnum = Field(index=True)
    is_default_address: bool = False

    # linkTable for User-Address Relationship
    user: "User" = Relationship(back_populates="user_addresses")
    address: "Address" = Relationship(back_populates="users")

    def __repr__(self):
        return f"<UserAddress(address_type={self.address_type} | default_address={self.is_default_address} | user_id={self.user_id})>"


class User(UUIDPrimaryKeyMixin, UserInfoMixin, TimestampMixin, SoftDeleteMixin, SQLModel, table=True):

    identity_verification: "IdentityVerification" = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys":"[IdentityVerification.user_id]"}
    )

    # a user can have more than one address(User-Address relationship)
    user_addresses: list[UserAddress] = Relationship(back_populates="user")

    # keeps record of all login information
    login_events: list["LoginEventInfo"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy":"selectin", "cascade":"all, delete-orphan"}
    )

    # keeps record of all login security information
    login_security: Optional["UserSecurityProfile"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy":"selectin", "cascade":"all, delete-orphan"}
    )

    organisations_created: list["Organisation"] = Relationship(
        back_populates="created_by_user",
        sa_relationship_kwargs={"foreign_keys":"[Organisation.created_by]", "lazy":"selectin", "cascade":"all, delete-orphan"}
    )

    # one user can belong to many organization(Organisation-User relationship)
    user_organisations: list["OrganisationMember"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy":"selectin", "cascade":"all, delete-orphan"}
    )

    # a user can perform many roles/have many roles assigned to it(User-Role relationship)
    role_assignments: list["RoleAssignment"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"foreign_keys":"[RoleAssignment.user_id]", "lazy":"selectin"}
    )

    def __repr__(self):
        return f"<User(id={self.id} | username={self.username})>"


class UserSecurityProfile(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    last_login: datetime= Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
            index=True
        )
    )

    failed_login_attempts: int = 0
    login_count: int = 0
    login_method: str | None = None
    locked_until: datetime | None = None
    password_changed_at: datetime | None = None

    # loginEvent-User relationship
    user_id: UUID = Field(foreign_key="user.id", unique=True, nullable=False, ondelete="CASCADE", index=True)
    user: User = Relationship(back_populates="login_security")

    def __repr__(self):
        return f"<UserSecurityProfile(id={self.id} | last_login={self.last_login})>"


class LoginEventInfo(UUIDPrimaryKeyMixin, SQLModel, table=True):
    occurred_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
            index=True
        )
    )
    ip_address: str | None = None
    device: str | None = None
    browser: str | None = None
    operating_system: str | None = None
    country: str | None = None
    city: str | None = None
    user_agent: str | None = None
    session_id_hash: str | None = None
    is_successful: bool = False

    # UserLogin-Security
    user_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    user: User = Relationship(back_populates="login_events")

    __table_args__ = (
        Index("idx_login_user_time", "user_id", "occurred_at"),
        Index("idx_login_success", "is_successful", "occurred_at"),
        Index("idx_login_ip", "ip_address"),
    )

    def __repr__(self):
        return f"<LoginEventInfo(id={self.id} | occurred_at={self.occurred_at})>"