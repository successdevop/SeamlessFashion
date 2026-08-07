from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr

from app.enums.user_enums import GenderEnum, AddressTypeEnum, VerificationStatusEnum, DocumentTypeEnum
from app.schemas.base_or_shared.orm_base import ORMBaseSchema


class VerificationDocumentCreate(BaseModel):
    verification_id: UUID
    document_type: DocumentTypeEnum
    expires_at: datetime | None = None


class VerificationBase(BaseModel):
    verification_status: VerificationStatusEnum
    user_id: UUID


class VerificationCreate(ORMBaseSchema, VerificationBase):
    documents: list[VerificationDocumentCreate] = Field(default_factory=list)


class VerificationRead(VerificationCreate):
    id: UUID


class VerificationReview(ORMBaseSchema, BaseModel):
    verification_status: VerificationStatusEnum
    verified_by: UUID
    verification_notes: str | None = None
    rejection_reason: str | None = None
    verified_at: datetime


class AdminVerificationDetails(VerificationRead):
    review: VerificationReview


class LoginEventData(ORMBaseSchema, BaseModel):
    ip_address: str
    device: str
    browser: str
    operating_system: str
    country: str
    city: str
    user_agent: str
    is_successful: bool = False


class LoginEventCreate(LoginEventData):
    session_id: str


class LoginEventRead(LoginEventData):
    id: UUID


class UserSecurityProfile(ORMBaseSchema, BaseModel):
    failed_login_attempts: int = 0
    login_count: int = 0
    login_method: str | None = None
    locked_until: datetime | None = None
    password_changed_at: datetime | None = None


class UserSecurityResponse(UserSecurityProfile):
    id: UUID


class UserBase(ORMBaseSchema, BaseModel):
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    username: str = Field(min_length=4, max_length=30)
    email: EmailStr
    phone_number: str
    avatar_url: str | None = None
    gender: GenderEnum | None = None
    date_of_birth: date | None = None


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserProfileUpdate(ORMBaseSchema, BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: str | None = None
    phone_number: str | None = None
    gender: GenderEnum | None = None
    date_of_birth: date | None = None


class AdminUserUpdate(ORMBaseSchema, BaseModel):
    is_active: bool | None = None
    email_verified: bool | None = None
    phone_verified: bool | None = None


class UserRead(UserBase):
    id: UUID
    is_active: bool
    email_verified: bool
    phone_verified: bool


class UserAddressCreate(ORMBaseSchema, BaseModel):
    address_type: AddressTypeEnum
    is_default_address: bool = False


class UserAddressRead(UserAddressCreate):
    user_id: UUID
    address_id: UUID

