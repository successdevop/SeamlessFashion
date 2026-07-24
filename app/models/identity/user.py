from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, DateTime, func

from sqlmodel import SQLModel, Field, Relationship

from app.enums.id_verification import VerificationStatuEnum, DocumentTypeEnum
from app.enums.user_enums import AddressTypeEnum
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin, UserInfoMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.base_models.base_tables import Address
    from app.models.identity.role import Role
    from app.models.organization.organisation import OrganisationMember


class IdentityVerification(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    verification_status: VerificationStatuEnum

    verified_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    submitted_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))

    verification_notes: str | None = None
    rejection_reason: str | None = None

    user_id: UUID = Field(foreign_key="user.id", unique=True, nullable=False)
    user: "User" = Relationship(
        back_populates="identity_verification",
        sa_relationship_kwargs={"foreign_keys":"[IdentityVerification.user_id]"}
    )

    verified_by: UUID | None = Field(default=None, foreign_key="user.id")
    verifier: "User" = Relationship(
        sa_relationship_kwargs={"foreign_keys":"[IdentityVerification.verified_by]"}
    )

    documents: list["IdentityDocument"] = Relationship(back_populates="verification", cascade_delete=True)


class IdentityDocument(UUIDPrimaryKeyMixin, table=True):
    document_type: DocumentTypeEnum
    document_number_encrypted: str
    document_url: str

    verification_id: UUID = Field(foreign_key="identityverification.id", ondelete="CASCADE")
    verification: IdentityVerification = Relationship(back_populates="documents")


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

    # linkTable for User-Address Relationship
    user: "User" = Relationship(back_populates="user_addresses")
    address: "Address" = Relationship(back_populates="users")


class UserRole(SQLModel, table=True):
    user_id: UUID = Field(
        foreign_key="user.id",
        primary_key=True
    )

    role_id: UUID = Field(
        foreign_key="role.id",
        primary_key=True
    )

    assigned_by: UUID = Field(foreign_key="user.id")
    assigned_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )

    user: "User" = Relationship(
        back_populates="user_roles",
        sa_relationship_kwargs={"foreign_keys":"[UserRole.user_id]"}
    ),

    assigned_by_user: "User" = Relationship(
        sa_relationship_kwargs={"foreign_keys":"[UserRole.assigned_by]"}
    )

    role: "Role" = Relationship(back_populates="users")


class User(UUIDPrimaryKeyMixin, UserInfoMixin, TimestampMixin, SoftDeleteMixin, SQLModel, table=True):

    identity_verification: IdentityVerification = Relationship(back_populates="user")

    # a user can perform many roles/have many roles assigned to it(User-Role relationship)
    user_roles: list[UserRole] = Relationship(back_populates="user")

    # a user can have more than one address(User-Address relationship)
    user_addresses: list[UserAddress] = Relationship(back_populates="user")

    # keeps record of all login information
    user_login_timelines: list["LoginEventInfo"] = Relationship(back_populates="user")

    # one user can belong to many organization(Organisation-User relationship)
    user_organisations: list["OrganisationMember"] = Relationship(back_populates="user")


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
    user: User = Relationship(back_populates="user_login_timelines")
