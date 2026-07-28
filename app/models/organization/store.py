from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKeyConstraint, Column, DateTime, func
from sqlmodel import SQLModel, Field, Relationship

from app.enums.currency import CurrencyEnum
from app.enums.org_enums import StoreStatusEnum
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models import Address, Organisation, OrganisationMember


class Store(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    name: str
    currency: CurrencyEnum
    timezone: str
    status: StoreStatusEnum

    created_by: UUID
    manager_id: UUID

    created_by_user: "OrganisationMember" = Relationship(
        back_populates="stores_created",
        sa_relationship_kwargs={"foreign_keys":"[Store.created_by]"}
    )
    manager: "OrganisationMember" = Relationship(sa_relationship_kwargs={"foreign_keys":"[Store.manager_id]"})

    store_staff: list["StoreStaff"] = Relationship(back_populates="store")

    # store-address relationship
    address_id: UUID | None= Field(foreign_key="address.id", unique=True)
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
        )
    )


class StoreStaff(SQLModel, table=True):
    staff_id: UUID = Field(foreign_key="organisation_member.user_id", primary_key=True)

    assigned_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    store_id: UUID = Field(foreign_key="store.id", primary_key=True)
    store: Store = Relationship(back_populates="store_staff")

    __table_args__ = (
        ForeignKeyConstraint(
            ["staff_id", "store_id"],
            ["organisation_member.user_id", "store.organisation_id"]
        )
    )