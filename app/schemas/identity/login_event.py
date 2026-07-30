from uuid import UUID

from pydantic import BaseModel

class LoginEventData(BaseModel):
    ip_address: str | None = None
    device: str | None = None
    browser: str | None = None
    operating_system: str | None = None
    country: str | None = None
    city: str | None = None
    user_agent: str | None = None
    session_id_hash: str | None = None
    is_successful: bool = False

    user_id: UUID
    

class LoginEventResponse(LoginEventData):
    id: UUID