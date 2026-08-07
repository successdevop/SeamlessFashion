from decimal import Decimal
from uuid import UUID

from pydantic import Field

from app.schemas.base_or_shared.orm_base import ORMBaseSchema


class AddressSummary(ORMBaseSchema):
    street: str = Field(min_length=3, max_length=255)
    city: str = Field(min_length=3, max_length=100)
    state: str = Field(min_length=3, max_length=100)
    country: str = Field(min_length=3, max_length=100)
    zip_postal_code: str | None = Field(default=None, min_length=5, max_length=20)


class AddressCreate(AddressSummary):
    pass


class AddressUpdate(ORMBaseSchema):
    street: str | None = Field(default=None, min_length=3, max_length=255)
    city: str | None = Field(default=None, min_length=3, max_length=255)
    state: str | None = Field(default=None, min_length=3, max_length=255)
    country: str | None = Field(default=None, min_length=3, max_length=255)
    zip_postal_code: str | None = Field(default=None, min_length=5, max_length=20)


class AddressLatLong(ORMBaseSchema):
    latitude: Decimal | None = Field(default=None, ge=90, le=90)
    longitude: Decimal | None = Field(default=None, ge=-180, le=180)


class AddressRead(AddressSummary):
    id: UUID


class AdminAddressInfo(AddressRead):
    coordinates: AddressLatLong