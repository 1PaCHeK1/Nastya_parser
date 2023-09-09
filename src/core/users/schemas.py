from pydantic import BaseModel, ConfigDict, Field
from datetime import date


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    tg_id: int | None


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str = Field(pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    tg_id: int = Field(gt=10 * 9 - 1, lt=10**10)


class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str = Field(pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    tg_id: int = Field(gt=10 * 9 - 1, lt=10**10)


class UserRegistrationApiDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(min_length=5, max_length=20)
    email: str
    password: str


class UserRegistrationTgDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tg_id: int = Field(gt=10 * 9 - 1, lt=10**10)


class RegistrationToken(BaseModel):
    id: int
    create_at: date

    class Config:
        orm_mode = True
