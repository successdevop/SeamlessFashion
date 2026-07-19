from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Relationship, Field

from app.enums.currency import CurrencyEnum
from app.enums.org_enums import OrganisationRoleEnum
from app.models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.base_tables import Address
    from app.models.app_users import User


class OrganisationMember(SQLModel, table=True):
    organisation_id: UUID = Field(foreign_key="organisation.id", primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    role: OrganisationRoleEnum
    employee_email: str

    joined_date: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )

    user: "User" = Relationship(back_populates="organisations")
    organisation: "Organisation" = Relationship(back_populates="users")


class Organisation(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    organisation_name: str
    logo_url: str | None = None
    business_email: str
    tax_number: str | None = None
    business_registration_number: str | None = None
    business_phone_no: str
    currency: CurrencyEnum

    address_id: UUID = Field(foreign_key="address.id")
    address: "Address" = Relationship(back_populates="organisation_address")

    # an organization can have many users (Organisation-User relationship)
    users: list[OrganisationMember] = Relationship(back_populates="organisation")
    # an organization can have many stores(Organisation-Store relationship)
    stores: list["Store"] = Relationship(back_populates="organisation")
    # an organization can have many warehouses(Organisation-Warehouse relationship)
    warehouses: list["Store"] = Relationship(back_populates="organisation")


class Store(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    currency: CurrencyEnum
    time_zone: timezone

    address_id: UUID = Field(foreign_key="address.id")
    address: "Address" = Relationship(back_populates="organisation_store")

    organisation_id: UUID = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship(back_populates="stores")


class WareHouse(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str
    capacity: float
    manager: UUID

    address_id: UUID = Field(foreign_key="address.id")
    address: "Address" = Relationship(back_populates="organisation_warehouse")

    organisation_id: UUID = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship(back_populates="warehouses")
