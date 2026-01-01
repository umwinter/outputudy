from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.user import UserPublic


class LoginRequest(BaseModel):
    email: EmailStr = Field(
        ..., description="ログイン用メールアドレス", examples=["alice@example.com"]
    )
    password: str = Field(..., description="パスワード", examples=["securepassword123"])

    model_config = ConfigDict(
        title="Login Request",
        json_schema_extra={
            "example": {"email": "alice@example.com", "password": "securepassword123"}
        },
    )


class LoginResponse(UserPublic):
    access_token: str = Field(
        ...,
        description="JWT アクセストークン",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    token_type: str = Field(
        default="bearer", description="トークンタイプ", examples=["bearer"]
    )

    model_config = ConfigDict(
        title="Login Response",
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Alice",
                "email": "alice@example.com",
                "access_token": "eyJhbGciOiJIUzI1Ni...",
                "token_type": "bearer",
            }
        },
    )


class RegisterRequest(BaseModel):
    name: str = Field(..., description="表示名", examples=["Alice"])
    email: EmailStr = Field(
        ..., description="登録用メールアドレス", examples=["alice@example.com"]
    )
    password: str = Field(..., description="パスワード", examples=["securepassword123"])

    model_config = ConfigDict(
        title="Registration Request",
        json_schema_extra={
            "example": {
                "name": "Alice",
                "email": "alice@example.com",
                "password": "securepassword123",
            }
        },
    )


class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="リセットリンク送信先メールアドレス",
        examples=["alice@example.com"],
    )

    model_config = ConfigDict(
        title="Forgot Password Request",
        json_schema_extra={"example": {"email": "alice@example.com"}},
    )


class ResetPasswordRequest(BaseModel):
    token: str = Field(
        ...,
        description="メールで受信したリセットトークン",
        examples=["reset-token-abc-123"],
    )
    new_password: str = Field(
        ..., description="新しいパスワード", examples=["newsecurepassword456"]
    )

    model_config = ConfigDict(
        title="Reset Password Request",
        json_schema_extra={
            "example": {
                "token": "reset-token-abc-123",
                "new_password": "newsecurepassword456",
            }
        },
    )


class MessageResponse(BaseModel):
    detail: str = Field(
        ...,
        description="実行結果の詳細メッセージ",
        examples=["Password has been reset successfully."],
    )

    model_config = ConfigDict(
        title="Message Response",
        json_schema_extra={"example": {"detail": "Action completed successfully."}},
    )
