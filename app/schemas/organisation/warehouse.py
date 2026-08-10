from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field

from app.enums.org_enums import StaffAssignmentStatus, WarehouseStatusEnum
from app.schemas.base_or_shared.address import AddressRead
from app.schemas.base_or_shared.orm_base import ORMBaseSchema

if TYPE_CHECKING:
    from app.schemas.organisation.organisation import OrganisationMemberSummary, OrganisationBase


class WarehouseStaffBase(ORMBaseSchema):
    staff_id: UUID
    organisation_id: UUID
    warehouse_id: UUID
    status: StaffAssignmentStatus


class WarehouseStaffSummary(WarehouseStaffBase):
    assigned_at: datetime
    removed_at: datetime | None = None
    assigned_by: UUID


class WarehouseBase(ORMBaseSchema):
    name: str
    warehouse_code: str
    max_storage_units: Decimal
    status: WarehouseStatusEnum


class WarehouseSummary(WarehouseBase):
    phone_number: str | None = None
    email: str | None = None


class WarehouseCreate(WarehouseSummary):
    pass


class WarehouseUpdate(ORMBaseSchema):
    name: str | None = None
    warehouse_code: str | None = None
    max_storage_units: Decimal | None = None
    status: WarehouseStatusEnum | None = None


class WarehouseRead(WarehouseSummary):
    id: UUID


class AdminWarehouseRead(WarehouseRead):
    created_by: UUID
    manager_id: UUID
    updated_by: UUID
    address_id: UUID
    organisation_id: UUID


class AdminWarehouseDetails(WarehouseRead):
    created_by_user: OrganisationMemberSummary
    manager: OrganisationMemberSummary
    warehouse_staff: list[WarehouseStaffSummary] = Field(default_factory=list)
    address: AddressRead
    organisation: OrganisationBase

