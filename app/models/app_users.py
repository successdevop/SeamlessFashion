import uuid
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, Relationship


class AddressBase(SQLModel):
    id: str = Field(
        default_factory=lambda : str(uuid.uuid4()),
        primary_key=True
    )
    street: str
    city: str
    state: str
    zipcode: str = Field(ge=6, le=6)


class Address(AddressBase, table=True):
    customer: list["Customer"] = Relationship(back_populates="address")
    employee: list["Employee"] = Relationship(back_populates="address")
    org_owner: list["Employee"] = Relationship(back_populates="address")
    warehouse_staff: list["Employee"] = Relationship(back_populates="address")
    delivery_partner: list["Employee"] = Relationship(back_populates="address")
    plt_owner: list["Employee"] = Relationship(back_populates="address")


class User(SQLModel):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(ge=3, le=12)
    email: str = Field(index=True, unique=True)
    email_verified: bool = False
    password_hash: str
    phone_number: str
    address_id: str | None = Field(default=None, foreign_key="address.id")

    created_at: datetime = Field(
        default_factory=lambda : datetime.now(tz=timezone.utc)
    )


class Customer(User, table=True):
    address: Address | None = Relationship(back_populates="customer")
    role: str = "customer"


class OrganisationOwner(User, table=True):
    address: Address | None = Relationship(back_populates="org_owner")
    role: str = "organisation_owner"


class Employee(User, table=True):
    address: Address | None = Relationship(back_populates="employee")
    role: str = "employee"
    organisation_role: str | None = None


class WarehouseStaff(User, table=True):
    address: Address | None = Relationship(back_populates="warehouse_staff")
    role: str = "warehouse_staff"


class DeliveryPartner(User, table=True):
    address: Address | None = Relationship(back_populates="delivery_partner")
    role: str = "delivery_partner"


class PlatformOwner(User, table=True):
    address: Address | None = Relationship(back_populates="plt_owner")
    role: str = "platform_owner"