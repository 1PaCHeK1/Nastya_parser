from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    tg_id: int

    class Config:
        orm_mode = True

class UserCreateSchema(BaseModel):
    username: str
    email: str = Field(regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    tg_id: int = Field(gt=10*9-1, lt=10**10)


class UserUpdateSchema(BaseModel):
    username: str
    email: str = Field(regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    tg_id: int = Field(gt=10*9-1, lt=10**10)
