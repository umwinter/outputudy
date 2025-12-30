from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.domain.models import User as UserDomain
from app.infrastructure.auth_middleware import get_current_user
from app.infrastructure.database import get_db
from app.infrastructure.repository.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from app.infrastructure.security import create_access_token
from app.service.auth_service import AuthService

router = APIRouter()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    id: str
    name: str
    email: str
    access_token: str
    token_type: str = "bearer"


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repo = SQLAlchemyUserRepository(db)
    return AuthService(repo)


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest, service: AuthService = Depends(get_auth_service)
) -> dict[str, str]:
    user = service.authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})

    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "access_token": access_token,
    }


@router.get("/me", response_model=LoginResponse)
async def read_users_me(
    current_user: UserDomain = Depends(get_current_user),
) -> dict[str, str]:
    return {
        "id": str(current_user.id),
        "name": current_user.name,
        "email": current_user.email,
        "access_token": "N/A",  # Token is not re-issued here for now
    }
