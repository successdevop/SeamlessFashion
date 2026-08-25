from typing import Any
from uuid import UUID

from app.notifications.email import EmailService


class EventDispatcher:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service

    async def dispatch(self, event_type: str, event_id: UUID, payload: dict[str, Any]):
        if event_type == "user.registration":
            self.email_service.send_email_with_html_template(
                recipients=payload["email"],
                email_subject="Email Verification",
                
            )