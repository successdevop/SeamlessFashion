from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKeyConstraint, Index
from sqlmodel import SQLModel, Field, Relationship

from app.enums.org_enums import WarehouseStatusEnum
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin
from base_models.base_models import StaffAssignmentMixin

if TYPE_CHECKING:
    from app.models import Address, Organisation, OrganisationMember


class Warehouse(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str
    warehouse_code: str
    max_storage_units: Decimal
    status: WarehouseStatusEnum

    created_by: UUID
    manager_id: UUID

    created_by_user: "OrganisationMember" = Relationship(
        back_populates="warehouses_created",
        sa_relationship_kwargs={"foreign_keys":"[Warehouse.created_by]"}
    )
    manager: "OrganisationMember" = Relationship(sa_relationship_kwargs={"foreign_keys":"[Warehouse.manager_id]"})

    warehouse_staff: list["WarehouseStaff"] = Relationship(back_populates="warehouse")

    # warehouse-address relationship
    address_id: UUID= Field(foreign_key="address.id")
    address: "Address" = Relationship(back_populates="warehouse")

    # warehouse-organisation relationship
    organisation_id: UUID = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship(back_populates="warehouses")

    __table_args__ = (
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
        Index("idx_warehouse_org", "organisation_id")
    )


class WarehouseStaff(StaffAssignmentMixin, SQLModel, table=True):
    warehouse_id: UUID = Field(primary_key=True)

    warehouse: Warehouse = Relationship(back_populates="warehouse_staff")
    staff: "OrganisationMember" = Relationship(
        back_populates="warehouse_assignments",
        sa_relationship_kwargs={"foreign_keys":"[WarehouseStaff.staff_id, WarehouseStaff.organisation_id]"}
    )
    assigned_by_employee: "OrganisationMember" = Relationship(
        sa_relationship_kwargs={"foreign_keys":"[WarehouseStaff.assigned_by]"}
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["staff_id", "organisation_id"],
            ["organisation_member.user_id", "organisation_member.organisation_id"]
        ),
        ForeignKeyConstraint(
            ["warehouse_id", "organisation_id"],
            ["warehouse.id", "warehouse.organisation_id"]
        )
    )