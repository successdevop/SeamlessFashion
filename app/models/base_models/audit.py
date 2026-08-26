from typing import Any
from uuid import UUID

from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field, Index

from app.models.base_models.base_models import UUIDPrimaryKeyMixin, TimestampMixin


class AuditLog(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    __tablename__ = "audit_log"

    actor_id: UUID = Field(foreign_key="user.id", index=True)
    audit_action: str  # CREATE, UPDATE, DELETE, LOGIN, etc.
    resource_type: str  # User, Organisation, Store, etc.
    resource_id: UUID = Field(index=True)
    old_state: dict[str, Any] = Field(sa_column=Column(JSON, nullable=True))  # JSON
    new_state: dict[str, Any] = Field(sa_column=Column(JSON, nullable=True))  # JSON
    ip_address: str | None = None
    user_agent: str | None = None
    metadata_changes: dict[str, Any] = Field(sa_column=Column(JSON, nullable=True))  # JSON - what specifically changed

    __table_args__ = (
        Index("idx_audit_user_time", "actor_id", "created_at"),
        Index("idx_audit_resource", "resource_type", "resource_id"),
        Index("idx_audit_action", "audit_action", "created_at"),
    )