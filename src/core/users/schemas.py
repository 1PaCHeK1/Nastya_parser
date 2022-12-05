from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    username: str
    email: str
    tg_id: int


class UserCreate(BaseModel):
    username: str
    email: str = Field(regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    tg_id: int = Field(gt=10*9-1, lt=10**10)


class UserUpdate(BaseModel):
    username: str
    email: str = Field(regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    tg_id: int = Field(gt=10*9-1, lt=10**10)
