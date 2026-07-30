from datetime import date

from pydantic import BaseModel, Field, EmailStr

from app.enums.user_enums import GenderEnum


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
    is_active: bool = False
    email_verified: bool = False
    phone_verified: bool = False
    identity_verified: bool = False


class UserResponse(UserBase):
    is_active: bool = False
    email_verified: bool = False
    phone_verified: bool = False
    identity_verified: bool = False


class UserDetails(UserResponse):
    pass
