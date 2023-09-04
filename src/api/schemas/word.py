from db.models import LanguageEnum

from .base import BaseSchema


class WordSchema(BaseSchema):
    id: int
    text: str
    language: LanguageEnum
