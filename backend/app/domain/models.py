from uuid import UUID

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: UUID
    name: str
    email: str
    hashed_password: str | None = None

    model_config = ConfigDict(from_attributes=True)
