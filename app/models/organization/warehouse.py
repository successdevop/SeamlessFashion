from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import SQLModel, Field, Relationship

from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.base_models.base_tables import Address
    from app.models.organization.organisation import Organisation


class WareHouse(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str
    warehouse_code: str
    max_storage_units: Decimal
    status: str
    created_by: UUID = Field(foreign_key="organisationmember.user_id")
    manager: UUID = Field(foreign_key="organisationmember.user_id")

    # warehouse-address relationship
    address_id: UUID = Field(foreign_key="address.id")
    address: "Address" = Relationship(back_populates="warehouses")

    # warehouse-organisation relationship
    organisation_id: UUID = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship(back_populates="warehouses")