from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.enums.user_enums import VerificationStatusEnum, DocumentTypeEnum


class VerificationSummary(BaseModel):
    verification_status: VerificationStatusEnum
    verified_at: datetime | None = None
    submitted_at: datetime | None = None
    verification_notes: str | None = None
    rejection_reason: str | None = None
    user_id: UUID
    verified_by: UUID | None = None


class VerificationDocument(BaseModel):
    verification_id: UUID

    document_type: DocumentTypeEnum
    document_number_encrypted: str
    document_number_hash: str
    storage_key: str | None = None

    file_size: int | None = None
    file_hash: str | None = None



