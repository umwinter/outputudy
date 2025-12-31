from structlog import get_logger

from app.core.config import settings
from app.domain.email import EmailService
from app.infrastructure.email.templates import render_email_template

logger = get_logger()


class ConsoleEmailService(EmailService):
    async def send_password_reset_email(self, to_email: str, token: str) -> None:
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        # Render template to verify it works (and usually looking at logs is enough)
        html_content = render_email_template(
            "email/password_reset.html", {"reset_link": reset_link}
        )

        logger.info(
            "email_simulation_send_password_reset",
            to_email=to_email,
            token=token,
            html_preview=html_content[:50],
        )
