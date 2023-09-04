from fastapi import Query
from typing import Annotated
from dataclasses import dataclass

from db.models import LanguageEnum


@dataclass
class WordFilterParams:
    language: Annotated[LanguageEnum, Query()]
    contain: str | None = Query(default=None)
