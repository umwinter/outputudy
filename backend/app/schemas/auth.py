from pydantic import BaseModel, EmailStr

from app.schemas.user import UserPublic


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(UserPublic):
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


class MessageResponse(BaseModel):
    detail: str
