from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field

from app.enums.currency import CurrencyEnum
from app.enums.org_enums import StoreStatusEnum, StaffAssignmentStatus
from app.schemas.base_or_shared.address import AddressRead
from app.schemas.base_or_shared.orm_base import ORMBaseSchema

if TYPE_CHECKING:
    from app.schemas.organisation.organisation import OrganisationMemberSummary, OrganisationBase


class StoreStaffBase(ORMBaseSchema):
    staff_id: UUID
    organisation_id: UUID
    store_id: UUID
    is_primary_store: bool = False
    status: StaffAssignmentStatus


class StoreStaffSummary(StoreStaffBase):
    assigned_at: datetime
    removed_at: datetime | None = None
    assigned_by: UUID


class StoreBase(ORMBaseSchema):
    name: str
    store_code: str
    timezone: str
    status: StoreStatusEnum


class StoreSummary(StoreBase):
    phone_number: str | None = None
    email: str | None = None


class StoreCreate(StoreSummary):
    pass


class StoreUpdate(ORMBaseSchema):
    name: str | None = None
    store_code: str | None = None
    timezone: str | None = None
    status: StoreStatusEnum | None = None
    updated_by: UUID


class StoreRead(StoreSummary):
    id: UUID


class AdminStoreRead(StoreRead):
    currency: CurrencyEnum
    created_by: UUID
    manager_id: UUID
    updated_by: UUID
    organisation_id: UUID
    address: AddressRead


class AdminStoreDetails(ORMBaseSchema):
    created_by_user: OrganisationMemberSummary
    manager: OrganisationMemberSummary
    store_staff: list[StoreStaffSummary] = Field(default_factory=list)
    address: AddressRead
    organisation: OrganisationBase