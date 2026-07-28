from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Relationship, Field

from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models import RolePermission


class Permission(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    code: str = Field(unique=True, index=True)
    module: str
    resource: str
    action: str
    description: str | None = None

    # a permission can have many roles performing it(Role-Permission relationship)
    roles: list["RolePermission"] = Relationship(back_populates="permission")
