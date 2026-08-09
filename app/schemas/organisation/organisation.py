from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field, EmailStr, HttpUrl

from app.enums.currency import CurrencyEnum
from app.enums.org_enums import SubscriptionPlanEnum, SubscriptionStatusEnum, MembershipStatus
from app.schemas.base_or_shared.address import AddressRead
from app.schemas.base_or_shared.orm_base import ORMBaseSchema

if TYPE_CHECKING:
    from app.schemas.organisation.store import StoreRead
    from app.schemas.organisation.warehouse import WarehouseRead


class OrganisationMemberBase(ORMBaseSchema):
    employee_email: str | None = None
    status: MembershipStatus


class OrganisationMemberSummary(OrganisationMemberBase):
    user_id: UUID
    organisation_id: UUID


class OrganisationMemberRead(OrganisationMemberSummary):
    joined_date: datetime
    left_date: datetime | None = None


class OrganisationBase(ORMBaseSchema):
    organisation_name: str
    email: EmailStr
    phone_number: str


class OrganisationSummary(OrganisationBase):
    logo_url: str | None = None
    tax_number: str | None = None
    business_registration_number: str | None = None
    website: HttpUrl | None = None
    industry: str | None = None
    description: str | None = None


class OrganisationSubscription(ORMBaseSchema):
    subscription_plan: SubscriptionPlanEnum


class OrganisationCreate(OrganisationSummary):
    pass


class OrganisationUpdate(ORMBaseSchema):
    organisation_name: str | None = None
    logo_url: str | None = None
    business_email: str | None = None
    website: str | None = None
    industry: str | None = None
    description: str | None = None
    updated_by: UUID


class OrganisationSubscriptionUpdate(ORMBaseSchema):
    subscription_plan: SubscriptionPlanEnum | None = None


class OrganisationRead(OrganisationSummary):
    id: UUID


class AdminOrganisationRead(OrganisationRead):
    created_by: UUID
    updated_by: UUID
    subscription_plan: SubscriptionPlanEnum
    subscription_status: SubscriptionStatusEnum
    currency: CurrencyEnum
    address: AddressRead


class AdminOrganisationDetails(ORMBaseSchema):
    employees: list[OrganisationMemberRead] = Field(default_factory=list)
    stores: list["StoreRead"] = Field(default_factory=list)
    warehouses: list["WarehouseRead"] = Field(default_factory=list)


class AdminOrganisationMemberDetails(ORMBaseSchema):
    user: "UserResponse"
    role_assignments: list["RoleAssignmentResponse"] = Field(default_factory=list)
    stores_created: list["StoreResponse"] = Field(default_factory=list)

    stores_managed: "StoreResponse"

    store_assignments: list["StoreStaffBase"] = Field(default_factory=list)

    warehouses_created: list["WarehouseResponse"] = Field(default_factory=list)
    warehouses_managed: list["WarehouseResponse"] = Field(default_factory=list)

    warehouse_assignments: list["WarehouseStaffBase"] = Field(default_factory=list)