from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, AnyHttpUrl, ConfigDict

from app.enums.user_enums import GenderEnum, UserRoleEnum, AddressTypeEnum
from app.schemas.base_or_shared.common import AddressData


class UserAddressResponse(BaseModel):
    address_id: UUID
    address_type: AddressTypeEnum
    is_default: bool
    address: AddressData


class UserRoleResponse(BaseModel):
    id: UUID
    role: UserRoleEnum
    assigned_by: UUID
    assigned_at: datetime


class UserLoginEventSummary(BaseModel):
    login_time: datetime
    successful: bool
    device: str
    browser: str


class AdminLoginEventSummary(UserLoginEventSummary):
    ip_address: str
    location: str
    operating_system: str
    country: str
    city: str
    user_agent: str
    session_id: str

    user_id: UUID


class OrganisationMemberData(BaseModel):
    id: UUID
    organisation_name: str
    joined_date: datetime


class UserBase(BaseModel):
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    username: str = Field(min_length=4, max_length=30)
    email: EmailStr
    phone_number: str
    avatar_url: AnyHttpUrl | None = None
    gender: GenderEnum | None = None
    date_of_birth: date | None = None


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: AnyHttpUrl | None = None
    phone_number: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)


class AdminUserUpdate(UserUpdate):
    is_active: bool | None = None
    is_verified: bool | None = None


class UserResponse(UserBase):
    id: UUID
    is_active: bool = False
    is_verified: bool = False
    last_login: datetime | None

    user_addresses: list[UserAddressResponse] = Field(default_factory=list)
    user_roles: list[UserRoleResponse] = Field(default_factory=list)
    user_organisations: list[OrganisationMemberData] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class UserAdminResponse(UserResponse):
    failed_login_attempts: int = 0
    login_count: int = 0
    login_method: str | None = None


    # put in another endpoint
    # user_login_timelines: list[LoginEventData] = Field(default_factory=list)
    # class PaginatedLoginEvents(BaseModel):
#     items: list[LoginEventData]
#     page: int
#     page_size: int
#     total: int
