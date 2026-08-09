from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field, Relationship

from app.enums.user_enums import VerificationStatusEnum, DocumentTypeEnum
from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models import User


class IdentityVerification(UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, SQLModel, table=True):
    verification_status: VerificationStatusEnum

    verified_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    submitted_at: datetime= Field(sa_column=Column(DateTime(timezone=True), nullable=True))

    verification_notes: str | None = None
    rejection_reason: str | None = None

    user_id: UUID = Field(foreign_key="user.id", unique=True, nullable=False, index=True)
    user: "User" = Relationship(
        back_populates="identity_verification",
        sa_relationship_kwargs={"foreign_keys":"[IdentityVerification.user_id]"}
    )

    verified_by: UUID | None = Field(default=None, foreign_key="user.id")
    verifier: "User | None" = Relationship(
        sa_relationship_kwargs={"foreign_keys":"[IdentityVerification.verified_by]"}
    )

    documents: list["IdentityDocument"] = Relationship(
        back_populates="verification",
        sa_relationship_kwargs={"lazy":"selectin"},
        cascade_delete=True
    )

    def __repr__(self):
        return f"<IdentityVerification(id={self.id} | submitted_at={self.submitted_at} | status={self.verification_status})>"


class IdentityDocument(UUIDPrimaryKeyMixin, SoftDeleteMixin, SQLModel, table=True):
    document_type: DocumentTypeEnum
    document_number_encrypted: str
    document_number_hash: str = Field(index=True)
    storage_key: str # Only certain roles should view / and also a short_lived signed url

    file_size: int
    file_hash: str# For integrity verification

    mime_type: str
    original_filename: str
    expires_at: datetime | None = None

    uploaded_at: datetime= Field(sa_column=Column(DateTime(timezone=True), nullable=True))

    verification_id: UUID = Field(foreign_key="identityverification.id", ondelete="CASCADE")
    verification: IdentityVerification = Relationship(back_populates="documents")

    def __repr__(self):
        return f"<IdentityDocument(id={self.id} | doc_type={self.document_type})>"