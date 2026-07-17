import uuid
from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field


class AddressBase(SQLModel):
    id: str = Field(
        default_factory=lambda : str(uuid.uuid4()),
        primary_key=True
    )
    street: str
    city: str
    state: str
    zipcode: str = Field(ge=6, le=6)



class User(SQLModel):
    id: UUID = Field(default_factory=lambda : uuid4(), primary_key=True)
    username: str = Field(ge=3, le=12)
    email: str = Field(index=True, unique=True)
    email_verified: bool = False
    password_hash: str
    phone_number: str
    address_id: str | None = Field(default=None, foreign_key="address.id")

    created_at: datetime = Field(
        default_factory=lambda : datetime.now(tz=timezone.utc)
    )
