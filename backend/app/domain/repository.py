from abc import ABC, abstractmethod

from .models import User


class UserRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def list_users(self) -> list[User]:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def create_user(self, name: str, email: str, hashed_password: str) -> User:
        pass

    @abstractmethod
    async def update_user_password(self, user_id: int, hashed_password: str) -> None:
        pass
