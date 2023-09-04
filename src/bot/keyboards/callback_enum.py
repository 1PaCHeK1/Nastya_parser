from enum import Enum

from aiogram.filters.callback_data import CallbackData
from pydantic import BaseModel


class CallbackDataEnum(str, Enum):
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


class BaseData(CallbackData, prefix="base"):
    enum: CallbackDataEnum


class QueryCallBack(BaseData, prefix="query"):
    data: str


class IdentCallBack(BaseData, prefix="ident"):
    data: int


class NavigationCallback(BaseData, prefix="navigation"):
    data: int
