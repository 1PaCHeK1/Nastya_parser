from enum import Enum
import json
from typing import Generic, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


_T = TypeVar("_T")

class CallbakDataEnum(str, Enum):
    favorites = "favorites"
    translate_word = "favorite-word"
    save_favorite = "save-favorite"
    next_page = "next-page"
    prev_page = "prev-page"
    quize_answer = "quize-answer"
    remove_favorite = "remove-favorite"

    registration = "registration"

    noop = "noop"


class PageNavigator(BaseModel):
    page_number: int = 0


class ObjectId(BaseModel):
    id: int


class Query(BaseModel):
    text: str



class CallbackData(GenericModel, Generic[_T]):
    enum: CallbakDataEnum
    data: _T = Field(default_factory=dict)
