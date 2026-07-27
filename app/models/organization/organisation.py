from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field, Relationship

from app.enums.currency import CurrencyEnum
from app.enums.org_enums import SubscriptionStatusEnum, SubscriptionPlanEnum, MembershipStatus
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models import User, Address, Store, Warehouse, RoleAssignment


class OrganisationMember(SQLModel, table=True):
    __tablename__ = "organisation_member"

    organisation_id: UUID = Field(
        foreign_key="organisation.id",
        primary_key=True
    )

    user_id: UUID = Field(
        foreign_key="user.id",
        primary_key=True
    )

    employee_email: str | None = None

    # User's status within the organization
    status: MembershipStatus
    joined_date: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )

    user: "User" = Relationship(back_populates="user_organisations")
    organisation: "Organisation" = Relationship(back_populates="employees")
    role_assignments: list["RoleAssignment"] = Relationship(back_populates="membership")


class Organisation(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
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

    # organisation-address relationship
    address_id: UUID | None = Field(foreign_key="address.id", unique=True)
    address: "Address" = Relationship(back_populates="organisation")

    # an organization can have more than one or many employees/organization member (Organisation-User relationship)
    employees: list[OrganisationMember] = Relationship(back_populates="organisation")
    # an organization can have more than one or many stores(Organisation-Store relationship)
    stores: list["Store"] = Relationship(back_populates="organisation")
    # an organization can have more than one or  many warehouses(Organisation-Warehouse relationship)
    warehouses: list["Warehouse"] = Relationship(back_populates="organisation")
