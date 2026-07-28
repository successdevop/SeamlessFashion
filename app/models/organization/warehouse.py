from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKeyConstraint
from sqlmodel import SQLModel, Field, Relationship

from app.enums.org_enums import WarehouseStatusEnum
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models import Address, Organisation, OrganisationMember


class Warehouse(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str
    warehouse_code: str
    max_storage_units: Decimal
    status: WarehouseStatusEnum

    created_by: UUID = Field(foreign_key="organisation_member.user_id")
    manager_id: UUID = Field(foreign_key="organisation_member.user_id")

    created_by_user: "OrganisationMember" = Relationship(
        back_populates="warehouses_created",
        sa_relationship_kwargs={"foreign_keys":"[Warehouse.created_by]"}
    )
    manager: "OrganisationMember" = Relationship(sa_relationship_kwargs={"foreign_keys":"[Warehouse.manager_id]"})

    # warehouse-address relationship
    address_id: UUID | None = Field(foreign_key="address.id", unique=True)
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
        )
    )