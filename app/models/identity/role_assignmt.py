from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, DateTime, func, ForeignKeyConstraint, Index, UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models import Role, User, OrganisationMember


class RoleAssignment(SQLModel, table=True):
    user_id: UUID = Field(primary_key=True)

    role_id: UUID = Field(
        foreign_key="role.id",
        primary_key=True
    )

    # For organization scoped roles (a default organization would be created for the platform to prevent null values
    # in organization id for platform role assignment)
    organisation_id: UUID = Field(primary_key=True)

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
        UniqueConstraint("user_id", "role_id", "organisation_id", name="uq_role_assignment"),

        ForeignKeyConstraint(
            [
                "user_id", "organisation_id"
            ],
            [
                "organisation_member.user_id", "organisation_member.organisation_id"
            ],
            name="fk_user_role_assignment_membership",
            ondelete="CASCADE"
        ),

        ForeignKeyConstraint(
            ["assigned_by", "organisation_id"],
            ["organisation_member.user_id", "organisation_member.organisation_id"],
            name="fk_assigner_role_assignment_membership"
        ),

        Index("idx_role_assign_active", "user_id", "is_active"),
        Index("idx_role_assign_valid", "valid_from", "valid_until"),
        Index("idx_role_role", "role_id"),
        Index("idx_role_org", "organisation_id")
    )

    def __repr__(self):
        return f"<RoleAssignment(user_id={self.user_id} | role_id={self.role_id} | is_active={self.is_active})>"
