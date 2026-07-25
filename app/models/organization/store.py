from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import SQLModel, Field, Relationship

from app.enums.currency import CurrencyEnum
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.base_models.base_tables import Address
    from app.models.organization.organisation import Organisation


class Store(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str
    currency: CurrencyEnum
    timezone: str
    status: str
    inventory: str
    
    created_by: UUID = Field(foreign_key="organisationmember.user_id")
    updated_by: UUID = Field(foreign_key="organisationmember.user_id")

    # store-address relationship
    address_id: UUID = Field(foreign_key="address.id")
    address: "Address" = Relationship(back_populates="stores")

    # store-organisation relationship
    organisation_id: UUID = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship(back_populates="stores")