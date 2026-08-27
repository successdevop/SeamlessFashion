from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, DateTime, func, ForeignKeyConstraint, Index, CheckConstraint
from sqlmodel import SQLModel, Field, Relationship

from app.models.base_models.base_models import UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models import Role, User, OrganisationMember


class RoleAssignment(UUIDPrimaryKeyMixin, SQLModel, table=True):
    # the user receiving the role
    user_id: UUID = Field(
        foreign_key="user.id",
        index=True
    )

    # the role being assigned
    role_id: UUID = Field(
        foreign_key="role.id",
        index=True
    )

    # organization in which the role is assigned
    organisation_id: UUID = Field(
        foreign_key="organisation.id",
        index=True
    )

    # user/member who assigns the role
    assigned_by_user_id: UUID

    # user/member organisation
    assigned_by_organisation_id: UUID

    # time role was assigned
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

    # expiry period
    valid_until: datetime | None = None

    # Role Status
    is_active: bool = Field(default=True, index=True)

    # Relationships
    # the organization member receiving the role
    membership: "OrganisationMember" = Relationship(
        back_populates="role_assignments",
        sa_relationship_kwargs={"foreign_keys":"[RoleAssignment.user_id, RoleAssignment.organisation_id]"}
    )

    # the role assigned
    role: "Role" = Relationship(back_populates="role_assignments")

    # Direct user relationship
    user: "User" = Relationship(
        back_populates="role_assignments",
        sa_relationship_kwargs={"foreign_keys":"[RoleAssignment.user_id]"}
    )
    # OrganisationMember who assigned the role
    assigned_by_member: "OrganisationMember" = Relationship(
        back_populates="roles_assigned",
        sa_relationship_kwargs={
            "foreign_keys":"[RoleAssignment.assigned_by_user_id, RoleAssignment.assigned_by_organisation_id]"
        }
    )

    __table_args__ = (
        CheckConstraint(
            "valid_until IS NULL OR valid_until > valid_from",
            name="ck_role_assignment_valid_period"
        ),

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
            ["assigned_by_user_id", "assigned_by_organisation_id"],
            ["organisation_member.user_id", "organisation_member.organisation_id"],
            name="fk_assigner_role_assignment_membership"
        ),

        Index("idx_role_assignment_org_role","organisation_id", "role_id"),
        Index("idx_role_assign_user_current", "user_id", "is_active"),
        Index("idx_role_assign_dates", "valid_from", "valid_until"),
        Index("idx_role_assign_user_role", "user_id", "role_id"),
        Index("idx_role_assign_active_period", "is_active", "valid_from", "valid_until"),
    )

    def __repr__(self):
        return f"<RoleAssignment(id={self.id} | role_id={self.role_id} | is_active={self.is_active})>"
