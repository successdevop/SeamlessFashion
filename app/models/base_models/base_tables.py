from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Index, CheckConstraint
from sqlmodel import SQLModel, Relationship

from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models import UserAddress, Organisation, Store, Warehouse


class Address(UUIDPrimaryKeyMixin, SoftDeleteMixin, TimestampMixin, SQLModel, table=True):
    street: str
    city: str
    state: str
    country: str
    zip_postal_code: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None

    # an address can have multiple users(User-Address relationship)
    users: list["UserAddress"] = Relationship(back_populates="address", sa_relationship_kwargs={"lazy":"selectin"})
    # organization address(Organisation-Address relationship)
    organisation: "Organisation | None" = Relationship(back_populates="address")
    # organization_store address(Store-Address relationship)
    store: "Store | None" = Relationship(back_populates="address")
    # organization_warehouse address(Warehouse-Address relationship)
    warehouse: "Warehouse | None" = Relationship(back_populates="address")

    __table_args__ = (
        CheckConstraint("latitude >= -90 AND latitude <= 90", name="check_latitude"),
        CheckConstraint("longitude >= -180 AND longitude <= 180", name="check_longitude"),
        CheckConstraint("LENGTH(zip_postal_code) <= 20", name="check_zip_length"),
        Index("idx_address_city_state", "city", "state"),
        Index("idx_address_country_zip", "country", "zip_postal_code"),
    )

    def __repr__(self):
        return f"<Address(id={self.id} | street={self.street}) | country={self.country})>"