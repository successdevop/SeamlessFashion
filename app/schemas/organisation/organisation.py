from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import Field, BaseModel

from app.enums.currency import CurrencyEnum
from app.schemas.base_or_shared.common import AddressData, OrganisationSharedInfo, StoreSharedInfo


class OrganisationRole(BaseModel):
    employee_id: UUID
    organisation_id: UUID
    role: str

    assigned_by: UUID
    assigned_at: datetime


class OrganisationMember(BaseModel):
    organisation_id: UUID
    user_id: UUID
    employee_email: str

    joined_date: datetime


class OrganisationBase(BaseModel):
    base: OrganisationSharedInfo
    logo_url: str | None = None
    tax_number: str | None = None
    business_registration_number: str | None = None
    business_phone_no: str
    currency: CurrencyEnum
    website: str | None = None
    industry: str | None = None
    description: str | None = None
    subscription_plan: str | None = None
    subscription_status: Literal["active", "not_active"] | None = "not_active"


class OrganisationResponse(OrganisationBase):
    id: UUID
    address: AddressData
    users: list[OrganisationMember] = Field(default_factory=list)
    stores: list[StoreSharedInfo] = Field(default_factory=list)
    warehouses: list["WareHouse"] = Field(default_factory=list)
    roles: list[OrganisationRole] = Field(default_factory=list)
