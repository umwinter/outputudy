from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import User
from app.infrastructure.database import get_db
from app.infrastructure.repository.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from app.service.user_service import UserService

router = APIRouter()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    repo = SQLAlchemyUserRepository(db)
    return UserService(repo)


@router.get("", response_model=list[User])
async def list_users(service: UserService = Depends(get_user_service)) -> list[User]:
    return await service.get_users()


@router.get("/{user_id}", response_model=User | None)
async def get_user(
    user_id: int, service: UserService = Depends(get_user_service)
) -> User | None:
    return await service.get_user_by_id(user_id)
