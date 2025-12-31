from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.domain.email import EmailService
from app.domain.models import User as UserDomain
from app.infrastructure.auth_middleware import get_current_user
from app.infrastructure.database import get_db
from app.infrastructure.email.console import ConsoleEmailService
from app.infrastructure.email.smtp import SMTPEmailService
from app.infrastructure.repository.sqlalchemy.user import (
    SQLAlchemyUserRepository,
)
from app.infrastructure.security import create_access_token, verify_access_token
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    LoginResponse,
    MessageResponse,
    RegisterRequest,
    ResetPasswordRequest,
)
from app.service.auth import AuthService

router = APIRouter()


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    repo = SQLAlchemyUserRepository(db)
    if settings.ENV == "test":
        email_service: EmailService = ConsoleEmailService()
    else:
        email_service = SMTPEmailService()
    return AuthService(repo, email_service)


@router.post("/login", response_model=LoginResponse, operation_id="login")
async def login(
    request: LoginRequest, service: AuthService = Depends(get_auth_service)
) -> LoginResponse:
    user = await service.authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})

    return LoginResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        access_token=access_token,
    )


@router.get("/me", response_model=LoginResponse, operation_id="get_current_user")
async def read_users_me(
    current_user: UserDomain = Depends(get_current_user),
) -> LoginResponse:
    return LoginResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        access_token="N/A",  # Token is not re-issued here for now
    )


@router.post("/register", response_model=LoginResponse, operation_id="register")
async def register(
    request: RegisterRequest, service: AuthService = Depends(get_auth_service)
) -> LoginResponse:
    try:
        user = await service.register_user(
            request.name, request.email, request.password
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})

    return LoginResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        access_token=access_token,
    )


@router.post(
    "/forgot-password", response_model=MessageResponse, operation_id="forgot_password"
)
async def forgot_password(
    request: ForgotPasswordRequest, service: AuthService = Depends(get_auth_service)
) -> MessageResponse:
    await service.request_password_reset(request.email)
    return MessageResponse(
        detail="If your email is registered, you will receive a reset link."
    )


@router.post(
    "/reset-password", response_model=MessageResponse, operation_id="reset_password"
)
async def reset_password(
    request: ResetPasswordRequest, service: AuthService = Depends(get_auth_service)
) -> MessageResponse:
    payload = verify_access_token(request.token)
    if not payload or payload.get("type") != "password_reset":
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid token")

    await service.reset_password(UUID(str(user_id)), request.new_password)
    return MessageResponse(detail="Password has been reset successfully.")
