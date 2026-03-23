from pydantic import BaseModel, ConfigDict
from uuid import UUID


class User(BaseModel):
    id: UUID
    email: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: str
    password: str
