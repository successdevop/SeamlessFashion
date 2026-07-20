from datetime import datetime
from typing import TYPE_CHECKING, Literal
from uuid import UUID

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field, Relationship

from app.enums.currency import CurrencyEnum
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.base_models.base_tables import Address
    from app.models.identity.user import User
    from app.models.organization.store import Store
    from app.models.organization.warehouse import WareHouse


class OrganisationRole(SQLModel, table=True):
    employee_id: UUID = Field(foreign_key="organisationmember.user_id", primary_key=True)
    organisation_id: UUID = Field(foreign_key="organisation.id", primary_key=True)
    role: str

    assigned_by: UUID = Field(foreign_key="organisationmember.user_id")
    assigned_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )

    # linkTable for organisationMember-Organisation relationship
    org_employee: "OrganisationMember" = Relationship(back_populates="organisation_roles")
    organisation: "Organisation" = Relationship(back_populates="roles")


class OrganisationMember(SQLModel, table=True):
    organisation_id: UUID = Field(foreign_key="organisation.id", primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    employee_email: str

    joined_date: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )

    # linkTable for User-Organisation relation
    user: "User" = Relationship(back_populates="user_organisations")
    organisation: "Organisation" = Relationship(back_populates="users")

    # one employee can have more than one role in an organization(OrganisationMember-Organisation relationship)
    organisation_roles: list[OrganisationRole] = Relationship(back_populates="org_employee")


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

    # an organization can have more than one or many users (Organisation-User relationship)
    users: list[OrganisationMember] = Relationship(back_populates="organisation")
    # an organization can have more than one or many stores(Organisation-Store relationship)
    stores: list["Store"] = Relationship(back_populates="organisation")
    # an organization can have more than one or  many warehouses(Organisation-Warehouse relationship)
    warehouses: list["WareHouse"] = Relationship(back_populates="organisation")
    # an organization can have an employee with more than one or many roles(OrganisationMember-Organisation relationship)
    roles: list[OrganisationRole] = Relationship(back_populates="organisation")
