from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import SQLModel, Field, Relationship

from app.enums.org_enums import WarehouseStatusEnum
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models import User, Address, Organisation


class Warehouse(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str
    warehouse_code: str
    max_storage_units: Decimal
    status: WarehouseStatusEnum

    created_by: UUID = Field(foreign_key="organisationmember.user_id")
    manager_id: UUID = Field(foreign_key="organisationmember.user_id")

    created_by_user: "User" = Relationship(sa_relationship_kwargs={"foreign_keys":"[Warehouse.created_by]"})
    manager: "User" = Relationship(sa_relationship_kwargs={"foreign_keys":"[Warehouse.manager_id]"})

    # warehouse-address relationship
    address_id: UUID | None = Field(foreign_key="address.id", unique=True)
    address: "Address" = Relationship(back_populates="warehouse")

    # warehouse-organisation relationship
    organisation_id: UUID = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship(back_populates="warehouses")