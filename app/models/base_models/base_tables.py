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
    user: list["UserAddress"] = Relationship(back_populates="address")
    # organization address(Organisation-Address relationship)
    organisations: "Organisation" = Relationship(back_populates="address")
    # organization_store address(Store-Address relationship)
    stores: "Store" = Relationship(back_populates="address")
    # organization_warehouse address(Warehouse-Address relationship)
    warehouses: "WareHouse" = Relationship(back_populates="address")




