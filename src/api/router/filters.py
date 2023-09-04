from dataclasses import dataclass
from typing import Annotated

from fastapi import Query

from db.models import LanguageEnum


@dataclass
class WordFilterParams:
    language: Annotated[LanguageEnum, Query()]
    contain: str | None = Query(default=None)
