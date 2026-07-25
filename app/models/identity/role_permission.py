from uuid import UUID

from sqlmodel import SQLModel, Field

from app.models.base_models.base_models import TimestampMixin


class RolePermission(SQLModel, table=True):
    role_id: UUID = Field(
        foreign_key="role.id",
        primary_key=True
    )

    permission_id: UUID = Field(
        foreign_key="permission.id",
        primary_key=True
    )

    is_allowed: bool = True
    # linkTable for Role-RolePermission Relationship