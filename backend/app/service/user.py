from uuid import UUID

from app.domain.models import User
from app.domain.repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_users(self) -> list[User]:
        return await self.user_repo.list_users()

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        return await self.user_repo.get_user_by_id(user_id)
