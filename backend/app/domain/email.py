from abc import ABC, abstractmethod


class EmailService(ABC):
    @abstractmethod
    async def send_password_reset_email(self, to_email: str, token: str) -> None:
        pass
