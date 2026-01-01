from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserPublic(BaseModel):
    id: UUID = Field(
        ...,
        description="ユーザー固有のUUID",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    name: str = Field(..., description="ユーザー名", examples=["Alice"])
    email: str = Field(
        ..., description="メールアドレス", examples=["alice@example.com"]
    )

    model_config = ConfigDict(
        from_attributes=True,
        title="User Public Information",
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Alice",
                "email": "alice@example.com",
            }
        },
    )
