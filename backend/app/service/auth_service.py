from datetime import timedelta

from app.domain.models import User
from app.domain.repository import UserRepository
from app.infrastructure.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def authenticate_user(self, email: str, password: str) -> User | None:
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            return None

        if not user.hashed_password:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    async def register_user(self, name: str, email: str, password: str) -> User:
        if await self.user_repo.get_user_by_email(email):
            raise ValueError("Email already registered")

        hashed_password = get_password_hash(password)
        return await self.user_repo.create_user(name, email, hashed_password)

    async def create_password_reset_token(self, email: str) -> str | None:
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            return None

        # Short-lived token for password reset (15 minutes)
        token = create_access_token(
            data={"sub": str(user.id), "type": "password_reset"},
            expires_delta=timedelta(minutes=15),
        )
        return token

    async def reset_password(self, user_id: int, new_password: str) -> None:
        hashed_password = get_password_hash(new_password)
        await self.user_repo.update_user_password(user_id, hashed_password)
