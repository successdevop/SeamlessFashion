from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr

from app.enums.user_enums import GenderEnum, AddressTypeEnum, VerificationStatusEnum, DocumentTypeEnum
from app.schemas.base_or_shared.address import AddressResponse
from app.schemas.base_or_shared.role_assignment import RoleAssignmentResponse
from app.schemas.organisation.organisation import OrganisationMemberBase


class VerificationDocument(BaseModel):
    verification_id: UUID

    document_type: DocumentTypeEnum
    document_number_encrypted: str
    document_number_hash: str
    storage_key: str | None = None

    file_size: int | None = None
    file_hash: str | None = None


class VerificationBase(BaseModel):
    verification_status: VerificationStatusEnum
    submitted_at: datetime
    user_id: UUID


class VerificationCreate(VerificationBase):
    documents: list[VerificationDocument] = Field(default_factory=list)


class VerificationReview(VerificationCreate):
    verification_id: UUID
    verification_status: VerificationStatusEnum
    verified_by: UUID
    verification_notes: str | None = None
    rejection_reason: str | None = None
    verified_at: datetime


class LoginEventData(BaseModel):
    ip_address: str | None = None
    device: str | None = None
    browser: str | None = None
    operating_system: str | None = None
    country: str | None = None
    city: str | None = None
    user_agent: str | None = None
    session_id_hash: str | None = None
    is_successful: bool = False

    user_id: UUID


class LoginEventResponse(LoginEventData):
    id: UUID


class UserSecurityProfile(BaseModel):
    failed_login_attempts: int = 0
    login_count: int = 0
    login_method: str | None = None
    locked_until: datetime | None = None
    password_changed_at: datetime | None = None

    user_id: UUID


class UserSecurityResponse(UserSecurityProfile):
    id: UUID


class UserBase(BaseModel):
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


class UserProfileUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: str | None = None
    phone_number: str | None = None
    gender: GenderEnum | None = None
    date_of_birth: date | None = None


class AdminUserUpdate(UserProfileUpdate):
    is_active: bool | None = None
    email_verified: bool | None = None
    phone_verified: bool | None = None
    identity_verified: bool | None = None


class UserResponse(UserBase):
    id: UUID
    is_active: bool = False
    email_verified: bool = False
    phone_verified: bool = False
    identity_verified: bool = False


class UserAddressResponse(BaseModel):
    user_id: UUID
    address_id: UUID
    address_type: AddressTypeEnum
    is_default_address: bool = False
    address: AddressResponse


class UserDetails(UserResponse):
    identity_verification: VerificationReview
    user_addresses: list[UserAddressResponse] = Field(default_factory=list)
    login_events: list[LoginEventResponse] = Field(default_factory=list)
    login_security: UserSecurityResponse
    user_organisations: list[OrganisationMemberBase] = Field(default_factory=list)
    role_assignments: list[RoleAssignmentResponse] = Field(default_factory=list)
