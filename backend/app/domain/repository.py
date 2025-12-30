from abc import ABC, abstractmethod

from .models import User


class UserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def list_users(self) -> list[User]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User | None:
        pass
