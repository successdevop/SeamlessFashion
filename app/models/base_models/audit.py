from typing import Any
from uuid import UUID

from sqlmodel import SQLModel, Field, Index

from base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin


class AuditLog(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    __tablename__ = "audit_log"

    actor_id: UUID = Field(foreign_key="user.id", index=True)
    action: str  # CREATE, UPDATE, DELETE, LOGIN, etc.
    resource_type: str  # User, Organisation, Store, etc.
    resource_id: UUID = Field(index=True)
    old_state: dict[str, Any] = None  # JSON
    new_state: dict[str, Any] = None  # JSON
    ip_address: str | None = None
    user_agent: str | None = None
    metadata_changes: dict[str, Any] = None  # JSON - what specifically changed

    __table_args__ = (
        Index("idx_audit_user_time", "user_id", "created_at"),
        Index("idx_audit_resource", "resource_type", "resource_id"),
        Index("idx_audit_action", "action", "created_at"),
    )