from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.enums.currency import CurrencyEnum
from app.enums.org_enums import StoreStatusEnum, StaffAssignmentStatus
from app.schemas.base_or_shared.address import AddressResponse
from app.schemas.organisation.organisation import OrganisationResponse, OrganisationMemberBase


class StoreStaffBase(BaseModel):
    staff_id: UUID
    organisation_id: UUID
    store_id: UUID
    is_primary_store: bool = False
    assigned_at: datetime
    removed_at: datetime | None = None
    assigned_by: UUID
    status: StaffAssignmentStatus


class StoreBase(BaseModel):
    name: str
    store_code: str
    currency: CurrencyEnum
    timezone: str
    status: StoreStatusEnum

    created_by: UUID
    manager_id: UUID | None = None
    updated_by: UUID | None = None
    address_id: UUID
    organisation_id: UUID


class StoreCreate(StoreBase):
    pass


class StoreUpdate(BaseModel):
    name: str | None = None
    store_code: str | None = None
    currency: CurrencyEnum | None = None
    timezone: str | None = None
    status: StoreStatusEnum | None = None
    updated_by: UUID
    manager_id: UUID | None = None
    address_id: UUID | None = None


class StoreResponse(StoreBase):
    id: UUID


class AdminStoreDetails(StoreBase):
    created_by_user: OrganisationMemberBase
    manager: OrganisationMemberBase
    store_staff: list[StoreStaffBase] = Field(default_factory=list)
    address: AddressResponse
    organisation: OrganisationResponse


class AdminStoreStaffDetails(StoreStaffBase):
    store: list[StoreResponse] = Field(default_factory=list)
    staff: OrganisationMemberBase
    assigned_by_employee: OrganisationMemberBase