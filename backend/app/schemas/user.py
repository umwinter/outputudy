from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserPublic(BaseModel):
    id: UUID
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)
