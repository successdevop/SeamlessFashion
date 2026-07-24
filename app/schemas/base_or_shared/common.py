from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.enums.currency import CurrencyEnum


class AddressData(BaseModel):
    id: UUID
    street: str
    city: str
    state: str
    country: str
    zip_postal_code: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None


class OrganisationSharedInfo(BaseModel):
    id: UUID
    organisation_name: str
    business_email: str


class StoreSharedInfo(BaseModel):
    id: UUID
    name: str
    currency: CurrencyEnum
    timezone: str
    status: str
    created_by: UUID


class WareHouseSharedInfo(BaseModel):
    id: UUID
    name: str
    warehouse_code: str
    max_storage_units: Decimal
    status: str