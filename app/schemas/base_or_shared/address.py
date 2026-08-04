from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base_or_shared.orm_base import ORMBaseSchema


class AddressSummary(BaseModel):
    street: str = Field(min_length=3, max_length=255)
    city: str = Field(min_length=3, max_length=100)
    state: str = Field(min_length=3, max_length=100)
    country: str = Field(min_length=3, max_length=100)
    zip_postal_code: str | None = Field(default=None, min_length=5, max_length=20)


class AddressCreate(AddressSummary):
    pass


class AddressUpdate(BaseModel):
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    zip_postal_code: str | None = None


class AddressRead(AddressSummary, ORMBaseSchema):
    id: UUID
    latitude: Decimal | None = None
    longitude: Decimal | None = None
