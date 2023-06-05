from .base import BaseSchema
from db.models import LanguageEnum


class WordSchema(BaseSchema):
    id: int
    text: str
    language: LanguageEnum
