from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    country: str
    zip_postal_code: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None


class AddressUpdate(BaseModel):
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    zip_postal_code: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None


class AddressResponse(AddressBase):
    id: UUID
