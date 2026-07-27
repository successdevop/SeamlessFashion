from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, DateTime, func, ForeignKeyConstraint
from sqlmodel import SQLModel, Field, Relationship

from app.models import OrganisationMember
from base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models import User, Role, Organisation


class RoleAssignment(SQLModel, table=True):
    user_id: UUID = Field(
        primary_key=True
    )

    role_id: UUID = Field(
        foreign_key="role.id",
        primary_key=True
    )

    # For organisation scoped roles
    organisation_id: UUID = Field(
        primary_key=True
    )

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

    __table_args__ = (
        ForeignKeyConstraint(
            [
                "user_id", "organisation_id"
            ],
            [
                "organisation_member.user_id", "organisation_member.organisation_id"
            ],
            name="fk_role_assignment_membership"
        ),
    )

    # Relationships
    membership: "OrganisationMember" = Relationship(
        back_populates="role_assignments",
    )

    role: "Role" = Relationship(back_populates="role_assignments")
