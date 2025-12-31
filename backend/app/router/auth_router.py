from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import User as UserDomain
from app.infrastructure.auth_middleware import get_current_user
from app.infrastructure.database import get_db
from app.infrastructure.email.console import ConsoleEmailService
from app.infrastructure.repository.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from app.infrastructure.security import create_access_token, verify_access_token
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


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    repo = SQLAlchemyUserRepository(db)
    email_service = ConsoleEmailService()
    return AuthService(repo, email_service)


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest, service: AuthService = Depends(get_auth_service)
) -> dict[str, str]:
    user = await service.authenticate_user(request.email, request.password)
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


@router.post("/register", response_model=LoginResponse)
async def register(
    request: RegisterRequest, service: AuthService = Depends(get_auth_service)
) -> dict[str, str]:
    try:
        user = await service.register_user(
            request.name, request.email, request.password
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})

    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "access_token": access_token,
    }


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest, service: AuthService = Depends(get_auth_service)
) -> dict[str, str]:
    await service.request_password_reset(request.email)
    return {"detail": "If your email is registered, you will receive a reset link."}


@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest, service: AuthService = Depends(get_auth_service)
) -> dict[str, str]:
    payload = verify_access_token(request.token)
    if not payload or payload.get("type") != "password_reset":
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid token")

    await service.reset_password(int(user_id), request.new_password)
    return {"detail": "Password has been reset successfully."}
