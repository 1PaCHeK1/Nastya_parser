from dataclasses import dataclass

from sqlalchemy import ColumnElement, and_

from db.models import LanguageEnum, Word


@dataclass
class WordCoreFilter:
    language: LanguageEnum
    contain: str | None = None

    def get_expression(self) -> ColumnElement[bool]:
        where_clause = and_(Word.language == self.language)
        if self.contain is not None:
            where_clause &= Word.text.contains(self.contain)
        return where_clause
