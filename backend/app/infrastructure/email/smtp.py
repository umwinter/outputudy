import logging
from email.message import EmailMessage

import aiosmtplib

from app.core.config import settings
from app.domain.email import EmailService
from app.infrastructure.email.templates import render_email_template

logger = logging.getLogger(__name__)


class SMTPEmailService(EmailService):
    def __init__(self) -> None:
        self.hostname = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.username = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL

    async def send_password_reset_email(self, to_email: str, token: str) -> None:
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        html_content = render_email_template(
            "email/password_reset.html", {"reset_link": reset_link}
        )

        message = EmailMessage()
        message["From"] = self.from_email
        message["To"] = to_email
        message["Subject"] = "Password Reset Request"

        message.set_content(html_content, subtype="html")

        try:
            await aiosmtplib.send(
                message,
                hostname=self.hostname,
                port=self.port,
                username=self.username,
                password=self.password,
                start_tls=settings.SMTP_TLS,
            )
            logger.info(f"Sent password reset email to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            raise
