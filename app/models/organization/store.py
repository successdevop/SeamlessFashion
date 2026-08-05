from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKeyConstraint, Index, UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

from app.enums.currency import CurrencyEnum
from app.enums.org_enums import StoreStatusEnum
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin, StaffAssignmentMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models import Address, Organisation, OrganisationMember


class Store(UUIDPrimaryKeyMixin, SoftDeleteMixin, TimestampMixin, SQLModel, table=True):
    name: str
    store_code: str = Field(index=True)
    currency: CurrencyEnum
    timezone: str
    status: StoreStatusEnum

    phone_number: str | None = Field(default=None)
    store_mail: str | None = Field(default=None, index=True)

    created_by: UUID = Field(index=True)
    manager_id: UUID | None = Field(default=None, index=True)

    updated_by: UUID | None = None

    created_by_user: "OrganisationMember" = Relationship(
        back_populates="stores_created",
        sa_relationship_kwargs={
            "primaryjoin":"and_("
                          "Store.created_by==OrganisationMember.user_id, "
                          "Store.organisation_id==OrganisationMember.organisation_id"
                          ")"
        }
    )

    manager: "OrganisationMember" = Relationship(
        back_populates="stores_managed",
        sa_relationship_kwargs={
            "primaryjoin":"and_("
                          "Store.manager_id==OrganisationMember.user_id, "
                          "Store.organisation_id==OrganisationMember.organisation_id"
                          ")"
        }
    )

    store_staff: list["StoreStaff"] = Relationship(
        back_populates="store", sa_relationship_kwargs={"lazy":"selectin"}
    )

    # store-address relationship
    address_id: UUID = Field(foreign_key="address.id")
    address: "Address" = Relationship(back_populates="store")

    # store-organisation relationship
    organisation_id: UUID = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship(back_populates="stores")

    __table_args__ = (
        UniqueConstraint("organisation_id", "store_code"),

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
        ForeignKeyConstraint(
            ["updated_by", "organisation_id"],
            ["organisation_member.user_id", "organisation_member.organisation_id"],
            name="fk_store_updated_by"
        ),
        Index("idx_store_org", "organisation_id"),
    )

    def __repr__(self):
        return f"<Store(id={self.id} | name={self.name})>"


class StoreStaff(StaffAssignmentMixin, SQLModel, table=True):
    staff_id: UUID = Field(primary_key=True)
    organisation_id: UUID = Field(primary_key=True)
    store_id: UUID = Field(primary_key=True)
    is_primary_store: bool = False

    store: Store = Relationship(
        back_populates="store_staff",
        sa_relationship_kwargs={
            "primaryjoin":"and_("
                          "StoreStaff.store_id==Store.id, "
                          "StoreStaff.organisation_id==Store.organisation_id"
                          ")"
        }
    )

    staff: "OrganisationMember" = Relationship(
        back_populates="store_assignments",
        sa_relationship_kwargs={"foreign_keys":"[StoreStaff.staff_id, StoreStaff.organisation_id]"}
    )

    assigned_by_employee: "OrganisationMember" = Relationship(
        sa_relationship_kwargs={"foreign_keys":"[StoreStaff.assigned_by, StoreStaff.organisation_id]"}
    )

    removed_by_employee: "OrganisationMember" = Relationship(
        sa_relationship_kwargs={"foreign_keys":"[StoreStaff.removed_by, StoreStaff.organisation_id]"}
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["staff_id", "organisation_id"],
            ["organisation_member.user_id", "organisation_member.organisation_id"]
        ),
        ForeignKeyConstraint(
            ["store_id", "organisation_id"],
            ["store.id", "store.organisation_id"]
        ),
        ForeignKeyConstraint(
            ["assigned_by", "organisation_id"],
            ["organisation_member.user_id", "organisation_member.organisation_id"]
        ),
        ForeignKeyConstraint(
            ["removed_by", "organisation_id"],
            ["organisation_member.user_id", "organisation_member.organisation_id"]
        ),

        Index("idx_store_staff","staff_id", "organisation_id"),
        Index("idx_store_staff_store", "store_id", "organisation_id"),
    )

    def __repr__(self):
        return f"<StoreStaff(staff_id={self.staff_id} | status={self.status})>"