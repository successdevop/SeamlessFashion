from typing import Any

from celery import Celery

from app.config.config import redis_settings
from app.notifications.email import EmailService

celery_app = Celery(
    "Seamless_Fashion_api_tasks",
    broker=redis_settings.redis_url(0),
    backend=redis_settings.redis_url(1)
)


@celery_app.task(bind=True, name="send_email_task")
def send_email_task(recipients: list, email_subject: str, template_name:str, template_data: dict[str, Any]):
    email_service = EmailService()
    sent_email = email_service.send_email_with_html_template(
        recipients=recipients, email_subject=email_subject, template_name=template_name, template_data=template_data
    )
    return sent_email