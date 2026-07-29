from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKeyConstraint, Index
from sqlmodel import SQLModel, Field, Relationship

from app.enums.currency import CurrencyEnum
from app.enums.org_enums import StoreStatusEnum
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin, StaffAssignmentMixin

if TYPE_CHECKING:
    from app.models import Address, Organisation, OrganisationMember


class Store(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str
    currency: CurrencyEnum
    timezone: str
    status: StoreStatusEnum

    created_by: UUID = Field(index=True)
    manager_id: UUID = Field(index=True)

    created_by_user: "OrganisationMember" = Relationship(
        back_populates="stores_created",
        sa_relationship_kwargs={"foreign_keys":"[Store.created_by]"}
    )
    manager: "OrganisationMember" = Relationship(sa_relationship_kwargs={"foreign_keys":"[Store.manager_id]"})

    store_staff: list["StoreStaff"] = Relationship(back_populates="store")

    # store-address relationship
    address_id: UUID= Field(foreign_key="address.id")
    address: "Address" = Relationship(back_populates="store")

    # store-organisation relationship
    organisation_id: UUID = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship(back_populates="stores")

    __table_args__ = (
        ForeignKeyConstraint(
            ["created_by", "organisation_id"],
            ["organisation_member.user_id", "organisation_member.organisation_id"],
            name="fk_store_creator_membership"
        ),
        ForeignKeyConstraint(
            ["manager_id", "organisation_id"],
            ["organisation_member.user_id", "organisation_member.organisation_id"],
            name="fk_store_manager_membership"
        ),
        Index("idx_store_org", "organisation_id")
    )


class StoreStaff(StaffAssignmentMixin, SQLModel, table=True):
    store_id: UUID = Field(primary_key=True)

    store: Store = Relationship(back_populates="store_staff")
    staff: "OrganisationMember" = Relationship(
        back_populates="store_assignments",
        sa_relationship_kwargs={"foreign_keys":"[StoreStaff.staff_id, StoreStaff.organisation_id]"}
    )

    assigned_by_employee: "OrganisationMember" = Relationship(
        sa_relationship_kwargs={"foreign_keys":"[StoreStaff.assigned_by]"}
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["staff_id", "organisation_id"],
            ["organisation_member.user_id", "organisation_member.organisation_id"]
        ),
        ForeignKeyConstraint(
            ["store_id", "organisation_id"],
            ["store.id", "store.organisation_id"]
        )
    )