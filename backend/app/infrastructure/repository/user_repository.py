from typing import List, Optional
from app.domain.models import User
from app.domain.repository import UserRepository

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users = [
            User(id=1, name="Alice", email="alice@example.com"),
            User(id=2, name="Bob", email="bob@example.com"),
        ]

    def get_user(self, user_id: int) -> Optional[User]:
        for user in self._users:
            if user.id == user_id:
                return user
        return None

    def list_users(self) -> List[User]:
        return self._users

    def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self._users:
            if user.email == email:
                return user
        return None
