from typing import Any
from uuid import UUID

from app.schemas.base_or_shared.orm_base import ORMBaseSchema


class AuditLogCreate(ORMBaseSchema):
    actor_id: UUID
    audit_action: str  # CREATE, UPDATE, DELETE, LOGIN, etc.
    resource_type: str  # User, Organisation, Store, etc.
    resource_id: UUID
    old_state: dict[str, Any] | None = None  # JSON
    new_state: dict[str, Any] | None = None  # JSON
    ip_address: str | None = None
    user_agent: str | None = None
    changes: dict[str, Any] | None = None  # JSON - what specifically changed