from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Index
from sqlmodel import SQLModel, Relationship, Field

from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models import RolePermission


class Permission(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    __tablename__ = "permission"

    code: str = Field(unique=True, index=True)
    module: str
    resource: str
    action: str
    description: str | None = None
    created_by: UUID = Field(foreign_key="user.id")

    # a permission can have many roles performing it(Role-Permission relationship)
    roles: list["RolePermission"] = Relationship(back_populates="permission", sa_relationship_kwargs={"lazy":"selectin"})

    __table_args__ = (
        Index("idx_permission_module","module"),
    )

    def __repr__(self):
        return f"<Permission(id={self.id} | code={self.code})>"
