from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field, EmailStr, model_validator, field_validator, HttpUrl, AnyHttpUrl, AnyUrl

from app.enums.user_enums import GenderEnum, AddressTypeEnum, VerificationStatusEnum, DocumentTypeEnum
from app.schemas.base_or_shared.orm_base import ORMBaseSchema
from app.utils.auth import validate_password
from app.utils.utils import validate_username, validate_phone_number, validate_date_of_birth

if TYPE_CHECKING:
    from app.schemas.base_or_shared.address import AddressRead


class VerificationDocumentCreate(ORMBaseSchema):
    document_type: DocumentTypeEnum
    expires_at: datetime | None = None


class VerificationDocumentRead(VerificationDocumentCreate):
    id: UUID


class VerificationBase(ORMBaseSchema):
    verification_status: VerificationStatusEnum
    user_id: UUID


class VerificationCreate(VerificationBase):
    documents: list[VerificationDocumentCreate] = Field(default_factory=list)


class VerificationRead(VerificationBase):
    id: UUID
    documents: list[VerificationDocumentRead]


class VerificationReview(ORMBaseSchema):
    verification_status: VerificationStatusEnum
    verified_by: UUID
    verification_notes: str | None = None
    rejection_reason: str | None = None
    verified_at: datetime

    @model_validator(mode="after")
    def validate_review(self):
        if self.verification_status == VerificationStatusEnum.REJECTED:
            if not self.rejection_reason:
                raise ValueError(
                    "rejection_reason is required when verification is rejected"
                )
        return self


class AdminVerificationDetails(VerificationBase):
    review: VerificationReview
    documents: list[VerificationDocumentRead]


class LoginEventSummary(ORMBaseSchema):
    ip_address: str | None = None
    device: str | None = None
    browser: str | None = None
    operating_system: str | None = None
    country: str | None = None
    city: str | None = None
    user_agent: str | None = None


class LoginEventCreate(LoginEventSummary):
    session_id: str


class LoginEventRead(LoginEventSummary):
    id: UUID
    is_successful: bool


class UserSecurityProfileSummary(ORMBaseSchema):
    failed_login_attempts: int = 0
    login_count: int = 0
    login_method: str | None = None
    locked_until: datetime | None = None
    password_changed_at: datetime | None = None


class UserSecurityRead(UserSecurityProfileSummary):
    id: UUID


class UserBase(ORMBaseSchema):
    username: str
    email: EmailStr
    phone_number: str

    @field_validator("username")
    @classmethod
    def validate_username_field(cls, value: str) -> str:
        return validate_username(value)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number_field(cls, value: str) -> str:
        return validate_phone_number(value)


class UserSummary(UserBase):
    avatar_url: HttpUrl | None = None
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    gender: GenderEnum | None = None
    date_of_birth: date | None = None

    @field_validator("avatar_url")
    @classmethod
    def normalize_avatar_url(cls, value: HttpUrl | AnyHttpUrl | AnyUrl) -> str | None:
        return str(value).strip().lower()

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob_field(cls, value: date) -> date | None:
        return validate_date_of_birth(value)


class UserCreate(UserSummary):
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def validate_password_field(cls, value: str):
        is_valid, message = validate_password(value)
        if not is_valid:
            raise ValueError(message)
        return value


class UserProfileUpdate(ORMBaseSchema):
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: HttpUrl | None = None
    phone_number: str | None = None
    gender: GenderEnum | None = None
    date_of_birth: date | None = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number_field(cls, value: str) -> str:
        return validate_phone_number(value)

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob_field(cls, value: date) -> date | None:
        return validate_date_of_birth(value)


class AdminUserProfileUpdate(ORMBaseSchema):
    is_active: bool | None = None
    email_verified: bool | None = None
    phone_verified: bool | None = None


class UserRead(UserSummary):
    id: UUID
    is_active: bool
    email_verified: bool
    phone_verified: bool


class UserAddressCreate(ORMBaseSchema):
    address_type: AddressTypeEnum
    is_default_address: bool = False


class UserAddressRead(UserAddressCreate):
    user_id: UUID
    address_id: UUID


class UserAddressDetails(UserAddressRead):
    address: "AddressRead"

