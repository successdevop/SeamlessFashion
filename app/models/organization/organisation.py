from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, DateTime, func, Index, UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

from app.enums.currency import CurrencyEnum
from app.enums.org_enums import SubscriptionStatusEnum, SubscriptionPlanEnum, MembershipStatus
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models import User, Address, Store, Warehouse, RoleAssignment, StoreStaff, WarehouseStaff


class OrganisationMember(SQLModel, table=True):
    __tablename__ = "organisation_member"

    employee_email: str | None = Field(default=None)
    employee_number: str = Field(unique=True, index=True)

    # User's status within the organization
    status: MembershipStatus
    joined_date: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )
    left_date: datetime | None = None

    user_id: UUID = Field(
        foreign_key="user.id",
        primary_key=True
    )

    organisation_id: UUID = Field(
        foreign_key="organisation.id",
        primary_key=True
    )

    user: "User" = Relationship(back_populates="user_organisations")

    organisation: "Organisation" = Relationship(back_populates="employees")

    role_assignments: list["RoleAssignment"] = Relationship(
        back_populates="membership",
        sa_relationship_kwargs={
            "foreign_keys":"[RoleAssignment.user_id], RoleAssignment.organisation_id",
            "lazy":"selectin", "cascade":"all, delete-orphan"
        }
    )

    roles_assigned: list["RoleAssignment"] = Relationship(
        back_populates="assigned_by_user",
        sa_relationship_kwargs={
            "foreign_keys":"[RoleAssignment.assigned_by, RoleAssignment.organisation_id]",
            "lazy":"selectin", "cascade":"all, delete-orphan"
        }
    )

    stores_created: list["Store"] = Relationship(
        back_populates="created_by_user",
        sa_relationship_kwargs={
            "foreign_keys": "[Store.created_by]", "lazy":"selectin"
        }
    )

    stores_managed: list["Store"] = Relationship(
        back_populates="manager",
        sa_relationship_kwargs={"foreign_keys":"[Store.manager_id]", "lazy":"selectin"}
    )

    store_assignments: list["StoreStaff"] = Relationship(
        back_populates="staff", sa_relationship_kwargs={"lazy":"selectin"}
    )

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

    __table_args__ = (
        UniqueConstraint(
            "user_id", "organisation_id", name="uq_org_member_user_org"
        ),
        Index("idx_org_member_status", "organisation_id", "status"),
        Index("idx_org_member_user_status", "user_id", "status"),
        Index("idx_org_member_joined", "joined_date"),
    )

    def __repr__(self):
        return f"<OrganisationMember(status={self.status} | joined_date={self.joined_date})>"


class Organisation(UUIDPrimaryKeyMixin, SoftDeleteMixin, TimestampMixin, SQLModel, table=True):
    organisation_name: str = Field(unique=True, index=True)
    logo_url: str | None = None
    email: str = Field(index=True, unique=True)
    tax_number: str | None = None
    business_registration_number: str | None = None
    phone_number: str
    currency: CurrencyEnum
    website: str | None = None
    industry: str | None = None
    description: str | None = None
    subscription_plan: SubscriptionPlanEnum
    subscription_status: SubscriptionStatusEnum

    created_by: UUID = Field(foreign_key="user.id")
    updated_by: UUID | None = Field(default=None, foreign_key="user.id")

    # organisation-address relationship
    address_id: UUID = Field(foreign_key="address.id")
    address: "Address" = Relationship(back_populates="organisation")

    created_by_user: "User" = Relationship(
        back_populates="organisations_created",
        sa_relationship_kwargs={"foreign_keys":"[Organisation.created_by]"}
    )

    updated_by_user: "User" = Relationship(
        sa_relationship_kwargs={"foreign_keys":"[Organisation.updated_by]"}
    )

    # an organization can have more than one or many employees/organization member (Organisation-User relationship)
    employees: list[OrganisationMember] = Relationship(
        back_populates="organisation", sa_relationship_kwargs={"lazy":"selectin"}
    )
    # an organization can have more than one or many stores(Organisation-Store relationship)
    stores: list["Store"] = Relationship(
        back_populates="organisation", sa_relationship_kwargs={"lazy":"selectin"}
    )
    # an organization can have more than one or  many warehouses(Organisation-Warehouse relationship)
    warehouses: list["Warehouse"] = Relationship(
        back_populates="organisation", sa_relationship_kwargs={"lazy":"selectin"}
    )

    def __repr__(self):
        return f"<Organisation(id={self.id} | name={self.organisation_name})>"
