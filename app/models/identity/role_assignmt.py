from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, DateTime, func, ForeignKeyConstraint, Index
from sqlmodel import SQLModel, Field, Relationship

from app.models.base_models.base_models import UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models import Role, User, OrganisationMember


class RoleAssignment(UUIDPrimaryKeyMixin, SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.id", index=True)

    role_id: UUID = Field(
        foreign_key="role.id",
        index=True
    )

    # For organization scoped roles (a default organization would be created for the platform to prevent null values
    # in organization id for platform role assignment)
    organisation_id: UUID = Field(foreign_key="organisation.id", index=True)

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
    is_active: bool = Field(default=True, index=True)

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

        Index("idx_role_assign_user_current", "user_id", "is_active"),
        Index("idx_role_assign_dates", "valid_from", "valid_until"),
        Index("idx_role_assign_user_role", "user_id", "role_id"),
        Index("idx_role_assign_active_period", "is_active", "valid_from", "valid_until"),
    )

    def __repr__(self):
        return f"<RoleAssignment(id={self.id} | role_id={self.role_id} | is_active={self.is_active})>"
