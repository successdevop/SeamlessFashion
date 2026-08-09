from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import SQLModel, Relationship, Field

from app.enums.org_enums import RoleScope
from app.models.base_models.base_models import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models import RolePermission, RoleAssignment


class Role(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    display_name: str | None = Field(default=None, index=True)
    name: str = Field(index=True)
    description: str | None = None
    scope: RoleScope = Field(index=True)

    hierarchy_level: int = 1  # Hierarchy level (1 = highest)
    
    is_system_role: bool = False
    is_assignable_role: bool = True

    created_by: UUID = Field(foreign_key="user.id")

    # a single role can have many permissions assigned to it to perform (Role-Permission relationship)
    permissions: list["RolePermission"] = Relationship(back_populates="role", sa_relationship_kwargs={"lazy":"selectin"})

    # a single role can have many users assigned to it(User-Role relationship)
    role_assignments: list["RoleAssignment"] = Relationship(back_populates="role", sa_relationship_kwargs={"lazy":"selectin"})

    def __repr__(self):
        return f"<Role(id={self.id} | name={self.name} | scope={self.scope})>"
