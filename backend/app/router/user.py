from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import User
from app.infrastructure.auth_middleware import get_current_user
from app.infrastructure.database import get_db
from app.infrastructure.repository.sqlalchemy.user import (
    SQLAlchemyUserRepository,
)
from app.schemas.user import UserPublic
from app.service.user import UserService

router = APIRouter()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    repo = SQLAlchemyUserRepository(db)
    return UserService(repo)


@router.get("", response_model=list[UserPublic])
async def list_users(
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> list[User]:
    return await service.get_users()


@router.get("/{user_id}", response_model=UserPublic | None)
async def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> User | None:
    return await service.get_user_by_id(user_id)
