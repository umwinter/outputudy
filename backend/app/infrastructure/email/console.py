import logging

from app.domain.email import EmailService

logger = logging.getLogger(__name__)


class ConsoleEmailService(EmailService):
    async def send_password_reset_email(self, to_email: str, token: str) -> None:
        logger.info(
            f"EMAIL SIMULATION: Sending password reset to {to_email} "
            f"with token: {token}"
        )
        print(
            f"EMAIL SIMULATION: Sending password reset to {to_email} "
            f"with token: {token}"
        )
