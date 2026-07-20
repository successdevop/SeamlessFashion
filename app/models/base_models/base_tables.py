from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Relationship

from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.identity.user import UserAddress
    from app.models.organization.organisation import Organisation
    from app.models.organization.store import Store
    from app.models.organization.warehouse import WareHouse


class Address(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    street: str
    city: str
    state: str
    country: str
    zip_postal_code: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None

    # an address can have multiple users(User-Address relationship)
    users: list["UserAddress"] = Relationship(back_populates="address")
    # organization address(Organisation-Address relationship)
    organisations: list["Organisation"] = Relationship(back_populates="address")
    # organization_store address(Store-Address relationship)
    stores: list["Store"] = Relationship(back_populates="address")
    # organization_warehouse address(Warehouse-Address relationship)
    warehouses: list["WareHouse"] = Relationship(back_populates="address")




