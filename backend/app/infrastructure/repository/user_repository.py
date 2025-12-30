from app.domain.models import User
from app.domain.repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._users = [
            User(id=1, name="Alice", email="alice@example.com"),
            User(id=2, name="Bob", email="bob@example.com"),
        ]

    def get_user_by_id(self, user_id: int) -> User | None:
        for user in self._users:
            if user.id == user_id:
                return user
        return None

    def list_users(self) -> list[User]:
        return self._users

    def get_user_by_email(self, email: str) -> User | None:
        for user in self._users:
            if user.email == email:
                return user
        return None
