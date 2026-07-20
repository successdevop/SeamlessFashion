from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Literal
from uuid import UUID

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Relationship, Field

from app.enums.currency import CurrencyEnum
from app.enums.org_enums import OrganisationRoleEnum
from app.models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.base_tables import Address
    from app.models.app_users import User


class OrganisationRoles(SQLModel, table=True):
    employee_id: UUID = Field(foreign_key="organisationmember.user_id", primary_key=True)
    organisation_id: UUID = Field(foreign_key="organisation.id", primary_key=True)
    name: OrganisationRoleEnum

    assigned_by: UUID = Field(foreign_key="organisationmember.user_id")
    assigned_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )

    # linkTable for organisationMember-Organisation relationship
    employee: "OrganisationMember" = Relationship(back_populates="emp_organisation")
    organisation: "Organisation" = Relationship(back_populates="employee")


class OrganisationMember(SQLModel, table=True):
    organisation_id: UUID = Field(foreign_key="organisation.id", primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    employee_email: str

    joined_date: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )

    # linkTable for User-Organisation relation
    user: "User" = Relationship(back_populates="organisations")
    organisation: "Organisation" = Relationship(back_populates="users")

    # one employee can have more than one role in an organization(OrganisationMember-Organisation relationship)
    emp_organisation: list[OrganisationRoles] = Relationship(back_populates="employee")


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
    subscription_plan: str | None = None
    subscription_status: Literal["active", "not_active"] | None = None
    
    # organisation-address relationship
    address_id: UUID = Field(foreign_key="address.id")
    address: "Address" = Relationship(back_populates="organisations")

    # an organization can have many users (Organisation-User relationship)
    users: list[OrganisationMember] = Relationship(back_populates="organisation")
    # an organization can have many stores(Organisation-Store relationship)
    stores: list["Store"] = Relationship(back_populates="organisation")
    # an organization can have many warehouses(Organisation-Warehouse relationship)
    warehouses: list["Store"] = Relationship(back_populates="organisation")
    # an organization can have an employee with many roles(OrganisationMember-Organisation relationship)
    employee: list[OrganisationRoles] = Relationship(back_populates="emp_organisation")


class Store(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str
    currency: CurrencyEnum
    timezone: str
    status: str
    created_by: UUID = Field(foreign_key="organisationmember.user_id")
    updated_by: UUID = Field(foreign_key="organisationmember.user_id")

    # store-address relationship
    address_id: UUID = Field(foreign_key="address.id")
    address: "Address" = Relationship(back_populates="stores")

    # store-organisation relationship
    organisation_id: UUID = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship(back_populates="stores")


class WareHouse(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str
    warehouse_code: str
    max_storage_units: Decimal
    status: str
    created_by: UUID = Field(foreign_key="organisationmember.user_id")
    manager: UUID = Field(foreign_key="organisationmember.user_id")

    # warehouse-address relationship
    address_id: UUID = Field(foreign_key="address.id")
    address: "Address" = Relationship(back_populates="warehouses")

    # warehouse-organisation relationship
    organisation_id: UUID = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship(back_populates="warehouses")
