from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import SQLModel, Field, Relationship

from app.enums.currency import CurrencyEnum
from app.enums.org_enums import StoreStatusEnum
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models import User, Address, Organisation


class Store(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str
    currency: CurrencyEnum
    timezone: str
    status: StoreStatusEnum

    created_by: UUID = Field(foreign_key="organisationmember.user_id")
    manager_id: UUID = Field(foreign_key="organisationmember.user_id")

    created_by_user: "User" = Relationship(sa_relationship_kwargs={"foreign_keys":"[Store.created_by]"})
    manager: "User" = Relationship(sa_relationship_kwargs={"foreign_keys":"[Store.manager_id]"})

    # store-address relationship
    address_id: UUID | None= Field(foreign_key="address.id", unique=True)
    address: "Address" = Relationship(back_populates="store")

    # store-organisation relationship
    organisation_id: UUID = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship(back_populates="stores")