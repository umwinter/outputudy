from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import User
from app.domain.repository import UserRepository
from app.infrastructure.orm_models import UserORM


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(UserORM).where(UserORM.id == user_id)
        result = await self.db.execute(stmt)
        user_orm = result.scalar_one_or_none()
        if user_orm:
            return User.model_validate(user_orm)
        return None

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(UserORM).where(UserORM.email == email)
        result = await self.db.execute(stmt)
        user_orm = result.scalar_one_or_none()
        if user_orm:
            return User.model_validate(user_orm)
        return None

    async def list_users(self) -> list[User]:
        stmt = select(UserORM)
        result = await self.db.execute(stmt)
        users_orm = result.scalars().all()
        return [User.model_validate(u) for u in users_orm]

    async def create_user(self, name: str, email: str, hashed_password: str) -> User:
        user_orm = UserORM(name=name, email=email, hashed_password=hashed_password)
        self.db.add(user_orm)
        await self.db.commit()
        await self.db.refresh(user_orm)
        return User.model_validate(user_orm)

    async def update_user_password(self, user_id: int, hashed_password: str) -> None:
        # Fetch first to update safely with ORM, or use update statement
        stmt = select(UserORM).where(UserORM.id == user_id)
        result = await self.db.execute(stmt)
        user_orm = result.scalar_one_or_none()
        if user_orm:
            user_orm.hashed_password = hashed_password  # type: ignore
            await self.db.commit()
