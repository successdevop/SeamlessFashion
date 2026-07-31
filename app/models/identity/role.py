from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Relationship, Field

from app.models.base_models.base_models import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models import RolePermission, RoleAssignment


class RoleScope(str, Enum):
    PLATFORM = "platform"
    ORGANISATION = "organisation"


class Role(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str = Field(index=True)
    description: str | None = None
    scope: RoleScope

    level: int = 1  # Hierarchy level (1 = highest)
    
    is_system_role: bool = False
    is_assignable_role: bool = True

    # a single role can have many permissions assigned to it to perform (Role-Permission relationship)
    permissions: list["RolePermission"] = Relationship(back_populates="role", sa_relationship_kwargs={"lazy":"selectin"})

    # a single role can have many users assigned to it(User-Role relationship)
    role_assignments: list["RoleAssignment"] = Relationship(back_populates="role", sa_relationship_kwargs={"lazy":"selectin"})

    def __repr__(self):
        return f"Role<({self.id} | {self.name} | {self.scope})>"
