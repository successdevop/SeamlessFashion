from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKeyConstraint, Index, UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

from app.enums.org_enums import WarehouseStatusEnum
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, StaffAssignmentMixin

if TYPE_CHECKING:
    from app.models import Address, Organisation, OrganisationMember


class Warehouse(UUIDPrimaryKeyMixin, SoftDeleteMixin, TimestampMixin, SQLModel, table=True):
    name: str
    warehouse_code: str = Field(index=True)
    max_storage_units: Decimal
    status: WarehouseStatusEnum

    phone_number: str | None = Field(default=None)
    email: str | None = Field(default=None, index=True)

    created_by: UUID = Field(index=True)
    manager_id: UUID = Field(index=True)

    updated_by: UUID | None = None

    created_by_user: "OrganisationMember" = Relationship(
        back_populates="warehouses_created",
        sa_relationship_kwargs={
            "primaryjoin":"and_("
                          "Warehouse.created_by==OrganisationMember.user_id, "
                          "Warehouse.organisation_id==OrganisationMember.organisation_id"
                          ")"
        }
    )
    manager: "OrganisationMember" = Relationship(
        back_populates="warehouses_managed",
        sa_relationship_kwargs={
            "primaryjoin":"and_("
                          "Warehouse.manager_id==OrganisationMember.user_id, "
                          "Warehouse.organisation_id==OrganisationMember.organisation_id"
                          ")"
        }
    )

    warehouse_staff: list["WarehouseStaff"] = Relationship(
        back_populates="warehouse", sa_relationship_kwargs={"lazy":"selectin"}
    )

    # warehouse-address relationship
    address_id: UUID = Field(foreign_key="address.id")
    address: "Address" = Relationship(back_populates="warehouse")

    # warehouse-organisation relationship
    organisation_id: UUID = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship(back_populates="warehouses")

    __table_args__ = (
        UniqueConstraint("organisation_id", "warehouse_code"),

        ForeignKeyConstraint(
            ["created_by", "organisation_id"],
            ["organisation_member.user_id", "organisation_member.organisation_id"],
            name="fk_warehouse_creator_membership"
        ),
        ForeignKeyConstraint(
            ["manager_id", "organisation_id"],
            ["organisation_member.user_id", "organisation_member.organisation_id"],
            name="fk_warehouse_manager_membership"
        ),
        ForeignKeyConstraint(
            ["updated_by", "organisation_id"],
            ["organisation_member.user_id", "organisation_member.organisation_id"],
            name="fk_warehouse_updated_by"
        ),
        Index("idx_warehouse_org", "organisation_id"),
    )

    def __repr__(self):
        return f"<Warehouse(id={self.id} | name={self.name})>"


class WarehouseStaff(StaffAssignmentMixin, SQLModel, table=True):
    staff_id: UUID = Field(primary_key=True)
    organisation_id: UUID = Field(primary_key=True)
    warehouse_id: UUID = Field(primary_key=True)

    warehouse: Warehouse = Relationship(
        back_populates="warehouse_staff",
        sa_relationship_kwargs={
            "primaryjoin":"and_("
                          "WarehouseStaff.warehouse_id==Warehouse.id, "
                          "WarehouseStaff.organisation_id==Warehouse.organisation_id"
                          ")"
        }
    )

    staff: "OrganisationMember" = Relationship(
        back_populates="warehouse_assignments",
        sa_relationship_kwargs={"foreign_keys":"[WarehouseStaff.staff_id, WarehouseStaff.organisation_id]"}
    )

    assigned_by_employee: "OrganisationMember" = Relationship(
        sa_relationship_kwargs={"foreign_keys":"[WarehouseStaff.assigned_by, WarehouseStaff.organisation_id]"}
    )

    removed_by_employee: "OrganisationMember" = Relationship(
        sa_relationship_kwargs={"foreign_keys":"[WarehouseStaff.removed_by, WarehouseStaff.organisation_id]"}
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["staff_id", "organisation_id"],
            ["organisation_member.user_id", "organisation_member.organisation_id"]
        ),
        ForeignKeyConstraint(
            ["warehouse_id", "organisation_id"],
            ["warehouse.id", "warehouse.organisation_id"]
        ),
        ForeignKeyConstraint(
            ["assigned_by", "organisation_id"],
            ["organisation_member.user_id", "organisation_member.organisation_id"]
        ),
        ForeignKeyConstraint(
            ["removed_by", "organisation_id"],
            ["organisation_member.user_id", "organisation_member.organisation_id"]
        ),

        Index("idx_warehouse_staff","staff_id", "organisation_id"),
        Index("idx_warehouse_staff_warehouse", "warehouse_id", "organisation_id"),
    )

    def __repr__(self):
        return f"<WarehouseStaff(staff_id={self.staff_id} | status={self.status})>"