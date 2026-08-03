from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.enums.currency import CurrencyEnum
from app.enums.org_enums import SubscriptionPlanEnum, SubscriptionStatusEnum, MembershipStatus
from app.schemas.identity.user import UserResponse
from app.schemas.organisation.store import StoreResponse, StoreStaffBase


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


class OrganisationResponse(OrganisationBase):
    id: UUID


class OrganisationDetails(OrganisationResponse):
    employees: list[OrganisationMemberBase] = Field(default_factory=list)
    stores: list[StoreResponse] = Field(default_factory=list)
    warehouses: list["Warehouse"] = Field(default_factory=list)


class AdminOrganisationMemberDetails(OrganisationMemberBase):
    user: UserResponse
    role_assignments: list["RoleAssignment"] = Relationship(
        back_populates="membership", sa_relationship_kwargs={"lazy":"selectin", "cascade":"all, delete-orphan"}
    )
    stores_created: list[StoreResponse] = Field(default_factory=list)

    stores_managed: StoreResponse

    store_assignments: list[StoreStaffBase] = Field(default_factory=list)

    warehouses_created: list["Warehouse"] = Relationship(
        back_populates="created_by_user",
        sa_relationship_kwargs={"foreign_keys":"[Warehouse.created_by]", "lazy":"selectin"}
    )

    warehouses_managed: list["Warehouse"] = Relationship(
        back_populates="manager",
        sa_relationship_kwargs={"foreign_keys":"[Warehouse.manager_id]", "lazy":"selectin"})

    warehouse_assignments: list["WarehouseStaff"] = Relationship(
        back_populates="staff", sa_relationship_kwargs={"lazy":"selectin"}
    )
    pass