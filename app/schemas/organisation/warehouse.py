from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, Field

from app.enums.org_enums import StaffAssignmentStatus, WarehouseStatusEnum

if TYPE_CHECKING:
    from app.schemas import OrganisationMemberBase, AddressResponse, OrganisationResponse



class WarehouseStaffBase(BaseModel):
    staff_id: UUID
    organisation_id: UUID
    warehouse_id: UUID
    assigned_at: datetime
    removed_at: datetime | None = None
    assigned_by: UUID
    status: StaffAssignmentStatus


class WarehouseBase(BaseModel):
    name: str
    warehouse_code: str
    max_storage_units: Decimal
    status: WarehouseStatusEnum
    created_by: UUID
    manager_id: UUID | None = None
    updated_by: UUID | None = None
    address_id: UUID
    organisation_id: UUID


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseUpdate(BaseModel):
    name: str
    warehouse_code: str
    max_storage_units: Decimal
    status: WarehouseStatusEnum
    updated_by: UUID
    manager_id: UUID | None = None
    address_id: UUID | None = None


class WarehouseResponse(WarehouseBase):
    id: UUID


class AdminWarehouseDetails(WarehouseResponse):
    created_by_user: "OrganisationMemberBase"
    manager: "OrganisationMemberBase"
    warehouse_staff: list[WarehouseStaffBase] = Field(default_factory=list)
    address: "AddressResponse"
    organisation: "OrganisationResponse"


class AdminWarehouseStaffDetails(WarehouseStaffBase):
    warehouse: WarehouseResponse
    staff: "OrganisationMemberBase"
    assigned_by_employee: "OrganisationMemberBase"
