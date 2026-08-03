from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, Field

from app.enums.currency import CurrencyEnum
from app.enums.org_enums import SubscriptionPlanEnum, SubscriptionStatusEnum, MembershipStatus

if TYPE_CHECKING:
    from app.schemas import StoreResponse, WarehouseResponse, UserResponse, RoleAssignmentResponse, StoreStaffBase, WarehouseStaffBase



class OrganisationMemberBase(BaseModel):
    organisation_id: UUID
    user_id: UUID

    employee_email: str | None = None

    status: MembershipStatus
    joined_date: datetime
    left_date: datetime | None = None


class OrganisationBase(BaseModel):
    organisation_name: str
    logo_url: str | None = None
    business_email: str
    tax_number: str | None = None
    business_registration_number: str | None = None
    business_phone_no: str
    currency: CurrencyEnum
    website: str | None = None
    industry: str | None = None
    description: str | None = None
    subscription_plan: SubscriptionPlanEnum
    subscription_status: SubscriptionStatusEnum
    address_id: UUID


class OrganisationCreate(OrganisationBase):
    pass


class OrganisationUpdate(BaseModel):
    organisation_name: str | None = None
    logo_url: str | None = None
    business_email: str | None = None
    tax_number: str | None = None
    business_registration_number: str | None = None
    business_phone_no: str | None = None
    currency: CurrencyEnum | None = None
    website: str | None = None
    industry: str | None = None
    description: str | None = None
    subscription_plan: SubscriptionPlanEnum | None = None
    subscription_status: SubscriptionStatusEnum | None = None
    address_id: UUID | None = None

class OrganisationResponse(OrganisationBase):
    id: UUID


class OrganisationDetails(OrganisationResponse):
    employees: list[OrganisationMemberBase] = Field(default_factory=list)
    stores: list["StoreResponse"] = Field(default_factory=list)
    warehouses: list["WarehouseResponse"] = Field(default_factory=list)


class AdminOrganisationMemberDetails(OrganisationMemberBase):
    user: "UserResponse"
    role_assignments: list["RoleAssignmentResponse"] = Field(default_factory=list)
    stores_created: list["StoreResponse"] = Field(default_factory=list)

    stores_managed: "StoreResponse"

    store_assignments: list["StoreStaffBase"] = Field(default_factory=list)

    warehouses_created: list["WarehouseResponse"] = Field(default_factory=list)
    warehouses_managed: list["WarehouseResponse"] = Field(default_factory=list)

    warehouse_assignments: list["WarehouseStaffBase"] = Field(default_factory=list)