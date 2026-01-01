from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import User
from app.infrastructure.auth_middleware import get_current_user
from app.infrastructure.database import get_db
from app.infrastructure.repository.sqlalchemy.user import (
    SQLAlchemyUserRepository,
)
from app.schemas.auth import MessageResponse
from app.schemas.user import UserPublic
from app.service.user import UserService

router = APIRouter()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    repo = SQLAlchemyUserRepository(db)
    return UserService(repo)


@router.get(
    "",
    response_model=list[UserPublic],
    responses={
        401: {"model": MessageResponse, "description": "未認証（ログインが必要です）"},
    },
    summary="ユーザー一覧取得",
    description="登録されているユーザーの一覧を取得します。認証済みのユーザーのみアクセス可能です。",
)
async def list_users(
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> list[User]:
    return await service.get_users()


@router.get(
    "/{user_id}",
    response_model=UserPublic | None,
    responses={
        401: {"model": MessageResponse, "description": "未認証（ログインが必要です）"},
        404: {"model": MessageResponse, "description": "ユーザーが見つかりません"},
    },
    summary="ユーザー詳細取得",
    description="IDを指定してユーザーの詳細情報を取得します。",
)
async def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> User | None:
    return await service.get_user_by_id(user_id)
