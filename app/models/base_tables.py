from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Relationship, Field

from app.models.app_organisations import Store
from app.models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.app_users import UserAddress
    from app.models.app_organisations import Organisation


class Address(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    street: str
    city: str
    state: str
    country: str
    zip_postal_code: str | None = Field(default=None, min_length=6, max_length=6)
    latitude: float | None = None
    longitude: float | None = None

    # an address can have multiple users(User-Address relationship)
    user: list["UserAddress"] = Relationship(back_populates="address")
    # organization address(Organisation-Address relationship)
    organisation_address: "Organisation" = Relationship(back_populates="address")
    # organization_store address(Store-Address relationship)
    organisation_store: "Store" = Relationship(back_populates="address")