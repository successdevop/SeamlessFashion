from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserSecurityProfile(BaseModel):
    failed_login_attempts: int = 0
    login_count: int = 0
    login_method: str | None = None
    locked_until: datetime | None = None
    password_changed_at: datetime | None = None

    user_id: UUID