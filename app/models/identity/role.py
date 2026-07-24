from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import SQLModel, Field, Relationship

from app.enums.user_enums import UserRoleEnum
from app.models.base_models.base_models import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.identity.user import UserRole
    from app.models.identity.permission import Permission


class RoleAssignment(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.id")
    role_id: UUID = Field(foreign_key="role.id")
    organisation_id: UUID = Field(foreign_key="Organisation.id")

    # linkTable for User-Role-Organisation Relationship
    


class RolePermission(TimestampMixin, SQLModel, table=True):
    role_id: UUID = Field(
        foreign_key="role.id",
        primary_key=True
    )

    permission_id: UUID = Field(
        foreign_key="permission.id",
        primary_key=True
    )
    # linkTable for Role-RolePermission Relationship


class Role(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: UserRoleEnum
    description: str | None = None
    is_system: bool = False

    # a single role can have many users assigned to it(User-Role relationship)
    users: list["UserRole"] = Relationship(back_populates="role")

    # a single role can have many permissions assigned to it to perform (Role-Permission relationship)
    permissions: list["Permission"] = Relationship(back_populates="roles", link_model=RolePermission)
