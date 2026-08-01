from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Index
from sqlmodel import SQLModel, Field, Relationship

from app.models.base_models.base_models import TimestampMixin

if TYPE_CHECKING:
    from app.models import Permission, Role


class RolePermission(TimestampMixin, SQLModel, table=True):
    role_id: UUID = Field(
        foreign_key="role.id",
        primary_key=True
    )

    permission_id: UUID = Field(
        foreign_key="permission.id",
        primary_key=True
    )

    assigned_by: UUID | None = Field(
        default=None,
        foreign_key="user.id"
    )
    
    # linkTable for Role-RolePermission Relationship
    role: "Role" = Relationship(back_populates="permissions")
    permission: "Permission" = Relationship(back_populates="roles")

    __table_args__ = (
        Index("idx_role_permission", "permission_id")
    )

    def __repr__(self):
        return f"<RolePermission(role_id={self.role_id} | permission_id{self.permission_id} | assigned_by_id{self.assigned_by})>"