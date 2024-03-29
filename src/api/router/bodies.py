from pydantic import BaseModel

from db.models import LanguageEnum


class WordInsertSchema(BaseModel):
    text: str
    language: LanguageEnum


class WordInsertWithTranslateSchema(WordInsertSchema):
    translates: list[WordInsertSchema]


class UserRegistrationSchema(BaseModel):
    email: str
    username: str
    password: str
