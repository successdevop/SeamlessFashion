from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field, Relationship

from app.enums.id_verification import VerificationStatuEnum, DocumentTypeEnum
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models import User


class IdentityVerification(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    verification_status: VerificationStatuEnum

    verified_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    submitted_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))

    verification_notes: str | None = None
    rejection_reason: str | None = None

    user_id: UUID | None = Field(default=None, foreign_key="user.id", unique=True)
    user: "User" = Relationship(
        back_populates="identity_verification",
        sa_relationship_kwargs={"foreign_keys":"[IdentityVerification.user_id]"}
    )

    verified_by_id: UUID | None = Field(default=None, foreign_key="user.id")
    verifier: "User" = Relationship(
        sa_relationship_kwargs={"foreign_keys":"[IdentityVerification.verified_by]"}
    )

    documents: list["IdentityDocument"] = Relationship(back_populates="verification", cascade_delete=True)


class IdentityDocument(UUIDPrimaryKeyMixin, table=True):
    document_type: DocumentTypeEnum
    document_number_encrypted: str
    document_url: str #Only certain roles should view

    verification_id: UUID = Field(foreign_key="identityverification.id", ondelete="CASCADE")
    verification: IdentityVerification = Relationship(back_populates="documents")