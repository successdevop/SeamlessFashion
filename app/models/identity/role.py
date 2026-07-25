from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Relationship

from app.models.base_models.base_models import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.identity.role_permission import RolePermission
    from app.models.identity.role_assignmt import RoleAssignment
    from app.models.identity.permission import Permission


class RoleScope(SQLModel):
    PLATFORM = "platform"
    ORGANISATION = "organisation"


class Role(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str
    description: str | None = None
    scope: RoleScope
    level: int  # Hierarchy level (1 = highest)
    is_system_role: bool = False
    is_assignable: bool

    # a single role can have many permissions assigned to it to perform (Role-Permission relationship)
    permissions: list["Permission"] = Relationship(back_populates="roles", link_model=RolePermission)

    # a single role can have many users assigned to it(User-Role relationship)
    role_assignments: list["RoleAssignment"] = Relationship(back_populates="role")
