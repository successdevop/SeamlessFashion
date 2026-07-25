from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Relationship

from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models import RolePermission


class Permission(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str
    module: str
    resource: str
    action: str
    description: str | None = None

    scope_type: str = "ANY" # "ANY", "OWN", "SPECIFIC"

    # a permission can have many roles performing it(Role-Permission relationship)
    roles: list["RolePermission"] = Relationship(back_populates="permission")
