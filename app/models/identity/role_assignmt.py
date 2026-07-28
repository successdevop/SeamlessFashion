from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, DateTime, func, ForeignKeyConstraint, Index, UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

from base_models.base_models import UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models import Role, User, OrganisationMember


class RoleAssignment(UUIDPrimaryKeyMixin, SQLModel, table=True):
    user_id: UUID

    role_id: UUID = Field(
        foreign_key="role.id",
    )

    # For organisation scoped roles
    organisation_id: UUID | None

    # Audit fields
    assigned_by: UUID = Field(foreign_key="user.id")

    assigned_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now()
        )
    )

    # Validity period
    valid_from: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now()
        )
    )
    valid_until: datetime | None = None

    # Status
    is_active: bool = True

    # Relationships
    membership: "OrganisationMember" = Relationship(
        back_populates="role_assignments",
    )

    role: "Role" = Relationship(back_populates="role_assignments")

    user: "User" = Relationship(
        back_populates="role_assignments",
        sa_relationship_kwargs={"foreign_keys":"[RoleAssignment.user_id]"}
    )

    assigned_by_user: "User" = Relationship(
        sa_relationship_kwargs={"foreign_keys":"[RoleAssignment.assigned_by]"}
    )

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", "organisation_id",
                         name="uq_role_assignment"
        ),

        ForeignKeyConstraint(
            [
                "user_id", "organisation_id"
            ],
            [
                "organisation_member.user_id", "organisation_member.organisation_id"
            ],
            name="fk_role_assignment_membership",
            ondelete="CASCADE"
        ),

        Index("idx_role_assign_active", "user_id", "is_active"),
        Index("idx_role_assign_valid", "valid_from", "valid_until"),
    )
