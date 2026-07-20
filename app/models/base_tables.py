from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import SQLModel, Relationship, Field

from app.enums.user_enums import UserRoleEnum
from app.models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.app_users import UserAddresses, UserRoles
    from app.models.app_organisations import Organisation, WareHouse, Store


class Address(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    street: str
    city: str
    state: str
    country: str
    zip_postal_code: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None

    # an address can have multiple users(User-Address relationship)
    user: list["UserAddresses"] = Relationship(back_populates="address")
    # organization address(Organisation-Address relationship)
    organisations: "Organisation" = Relationship(back_populates="address")
    # organization_store address(Store-Address relationship)
    stores: "Store" = Relationship(back_populates="address")
    # organization_warehouse address(Warehouse-Address relationship)
    warehouses: "WareHouse" = Relationship(back_populates="address")


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
    users: list[UserRoles] = Relationship(back_populates="role")

    # a single role can have many permissions assigned to it to perform (Role-Permission relationship)
    permissions: list["Permission"] = Relationship(back_populates="roles", link_model=RolePermission)


class Permission(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str
    module: str
    resource: str
    action: str
    description: str | None = None

    # a permission can have many roles performing it(Role-Permission relationship)
    roles: list[Role] = Relationship(back_populates="permissions", link_model=RolePermission)