from __future__ import annotations
from datetime import datetime

import enum
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey, Enum
from db.base import Base
from db.types import int_pk, text

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.models import User


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int_pk]
    name: Mapped[str]
    order: Mapped[int] = mapped_column(default=1)


class LanguageEnum(str, enum.Enum):
    ru = "ru"
    en = "en"


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int_pk]
    text: Mapped[str]

    language: Mapped[LanguageEnum] = mapped_column(
        Enum(LanguageEnum, native_enum=False),
        insert_default=LanguageEnum.ru,
        default=LanguageEnum.ru.value,
    )
    favorite_for_users: Mapped[list[User]] = relationship(
        secondary="favoriteword",
        back_populates="favorite_words",
    )
    # translates: list["Word"] = association_proxy(
    #     "translates_association",
    #     "word_to",
    # )


class WordTranslate(Base):
    __tablename__ = "wordtranslates"

    word_from_id: Mapped[int] = mapped_column(ForeignKey("words.id", ondelete="CASCADE"), primary_key=True)
    word_to_id: Mapped[int] = mapped_column(ForeignKey("words.id", ondelete="CASCADE"), primary_key=True)

    # word_from: Mapped[Word] = relationship(
    #     Word,
    #     primaryjoin="foreign(WordTranslate.word_from_id) == Word.id",
    # )
    # word_to: Mapped[Word] = relationship(
    #     Word,
    #     primaryjoin="foreign(WordTranslate.word_to_id) == Word.id",
    # )


class FavoriteWord(Base):
    __tablename__ = "favoriteword"

    id: Mapped[int_pk]

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"),
        primary_key=True,
    )


class RightAnswerEnum(str, enum.Enum):
    answer_one = "answer_one"
    answer_two = "answer_two"
    answer_three = "answer_three"


class QuizQuestion(Base):
    __tablename__ = "quizquestions"

    id: Mapped[int_pk]

    question: Mapped[str]
    theme_id: Mapped[int] = mapped_column(ForeignKey('quiztheme.id', ondelete="CASCADE"))
    answer_one: Mapped[str]
    answer_two: Mapped[str]
    answer_three: Mapped[str]
    right_answer: Mapped[RightAnswerEnum] = mapped_column(
        Enum(
            RightAnswerEnum,
            default=RightAnswerEnum.answer_one.value,
            native_enum=False,
        ),
    )


class QuizTheme(Base):
    __tablename__ = "quiztheme"

    id: Mapped[int_pk]
    name: Mapped[str]
