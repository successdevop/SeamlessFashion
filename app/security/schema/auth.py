from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ORMBaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )


@dataclass(frozen=True, slots=True)
class CurrentAuth:
    user_id: UUID
    session_id: UUID
    token_id: UUID


@dataclass(frozen=True)
class SigningKey:
    kid: str
    private_key: str
    public_key: str
    algorithm: str


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


class AuthSessionStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"


class AuthSessionRead(ORMBaseSchema):
    id: UUID
    status: AuthSessionStatus
    created_at: datetime
    last_used_at: datetime | None
    device_name: str | None


class AdminAuthSessionRead(ORMBaseSchema):
    id: UUID
    user_id: UUID
    family_token_id: UUID
    status: AuthSessionStatus
    created_at: datetime
    expires_at: datetime
    last_used_at: datetime | None
    revoked_at: datetime | None
    revoked_reason: str | None
    device_name: str | None
    user_agent: str | None
    ip_address: str | None