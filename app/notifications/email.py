from pathlib import Path
from typing import Any

from fastapi import UploadFile
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.config.config import email_settings


TEMPLATE_DIR=Path(__name__).resolve().parent.joinpath("email_templates")


class EmailService:
    def __init__(self):
        self._config = ConnectionConfig(
            **email_settings.model_dump(),
            TEMPLATE_FOLDER=TEMPLATE_DIR
        )
        self._fastmail = FastMail(config=self._config)
        self._email_sender = self._fastmail.send_message

    async def send_email_with_html_template(
            self, recipients: list, email_subject: str,
            template_name:str,
            template_data: dict[str, Any],
            attachments: list[UploadFile] | None = None
    ):
        try:
            message=MessageSchema(
                recipients=recipients,
                subject=email_subject,
                template_body=template_data,
                attachments=attachments,
                subtype=MessageType.html
            )

            await self._email_sender(
                message=message,
                template_name=template_name
            )
        except Exception as e:
            raise e
