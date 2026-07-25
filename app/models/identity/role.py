from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Relationship, Field

from app.models.base_models.base_models import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models import RolePermission, RoleAssignment


class RoleScope(SQLModel):
    PLATFORM = "platform"
    ORGANISATION = "organisation"


class Role(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str
    description: str | None = None
    scope: RoleScope

    level: int = 10  # Hierarchy level (1 = highest)
    is_system_role: bool = False
    is_assignable_role: bool = True

    # For organization-scoped roles, if they can be created by users
    is_custom: bool = Field(default=False)

    # a single role can have many permissions assigned to it to perform (Role-Permission relationship)
    permissions: list["RolePermission"] = Relationship(back_populates="role")

    # a single role can have many users assigned to it(User-Role relationship)
    role_assignments: list["RoleAssignment"] = Relationship(back_populates="role")
