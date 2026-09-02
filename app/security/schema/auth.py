from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


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