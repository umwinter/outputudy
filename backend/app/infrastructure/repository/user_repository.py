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

    def create_user(self, name: str, email: str, hashed_password: str) -> User:
        new_id = max(u.id for u in self._users) + 1 if self._users else 1
        user = User(id=new_id, name=name, email=email, hashed_password=hashed_password)
        self._users.append(user)
        return user

    def update_user_password(self, user_id: int, hashed_password: str) -> None:
        for user in self._users:
            if user.id == user_id:
                user.hashed_password = hashed_password
                return
