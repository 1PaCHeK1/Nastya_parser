import random
from collections.abc import Sequence

import langid
import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from core.caches.services import RedisService
from core.users.schemas import UserSchema
from core.words.dto import WordCoreFilter
from core.words.schemas import WordCreateSchema
from db.models import (
    FavoriteWord,
    LanguageEnum,
    QuizQuestion,
    Word,
    WordTranslate,
    QuizTheme,
)
from parsers.translate_word import TranslateWordService


# redis -> database -> wooordhunt
class WordService:
    page_size: int = 2

    def __init__(
        self,
        parser_service: TranslateWordService,
        cache_service: RedisService,
        session: Session,
    ) -> None:
        langid.set_languages([enum.name for enum in LanguageEnum])
        self.parser_service = parser_service
        self.cache_service = cache_service
        self._session = session

    async def get_words(
        self,
        filter_: WordCoreFilter,
    ) -> Sequence[Word]:
        stmt = select(Word).where(filter_.get_expression())
        return self._session.scalars(stmt).all()

    async def get_translate_by_id(
        self,
        user: UserSchema,
        word_id: int,
    ) -> list[str]:
        TranslateWord = sa.orm.util.AliasedClass(Word)
        words = self._session.scalars(
            select(Word.text, TranslateWord.text.label("translate_word"))
            .join(
                WordTranslate,
                (Word.id == WordTranslate.word_from_id)
                | (Word.id == WordTranslate.word_to_id),
            )
            .join(
                TranslateWord,
                (
                    (TranslateWord.id == WordTranslate.word_from_id)
                    & (Word.id == WordTranslate.word_to_id)
                )
                | (
                    (Word.id == WordTranslate.word_from_id)
                    & (TranslateWord.id == WordTranslate.word_to_id)
                ),
            )
            .where(Word.id == word_id),
        )
        return [word.translate_word for word in words]

    async def get_translate(
        self,
        user: UserSchema,
        word: str,
    ) -> list[str]:
        print("find in redis")
        translate_words = None and await self.cache_service.get_translate(user, word)
        if translate_words:
            return translate_words

        print("find in database")
        TranslateWord = sa.orm.util.AliasedClass(Word)
        translate_words = self._session.scalars(
            select(Word.text, TranslateWord.text.label("translate_word"))
            .join(
                WordTranslate,
                (Word.id == WordTranslate.word_from_id)
                | (Word.id == WordTranslate.word_to_id),
            )
            .join(
                TranslateWord,
                (
                    (TranslateWord.id == WordTranslate.word_from_id)
                    & (Word.id == WordTranslate.word_to_id)
                )
                | (
                    (Word.id == WordTranslate.word_from_id)
                    & (TranslateWord.id == WordTranslate.word_to_id)
                ),
            )
            .where(Word.text == word),
        )
        translate_words = [
            translate_word.translate_word for translate_word in translate_words
        ]

        if translate_words == []:
            print("find in site")
            translate_words = await self.parser_service.get_translate(word)

        await self.append_word(word)
        await self.cache_service.set_translate(word, translate_words)
        return translate_words

    async def get_phrases(self, word: str) -> str:
        ...

    async def get_examples(self, word: str) -> str:
        ...

    async def append_word(self, word: WordCreateSchema) -> None:
        language_code = langid.classify(word.word)
        main_word = Word(
            text=word.word,
            language=LanguageEnum[language_code],
        )
        self._session.add(main_word)
        self._session.flush()
        for word_translate in word.translate_words:
            language_code = langid.classify(word_translate)
            translate = Word(
                text=word_translate,
                language=LanguageEnum[language_code],
            )
            self._session.add(translate)
            self._session.flush()
            wordtranslate = WordTranslate(
                word_from_id=main_word.id,
                word_to_id=translate.id,
            )
            self._session.add(wordtranslate)
            self._session.flush()

    async def add_favorite(self, word_text: str, user: UserSchema):
        word = self._session.scalar(select(Word).where(Word.text == word_text))
        favoriteword = FavoriteWord(
            user_id=user.id,
            word_id=word.id,
        )
        self._session.add(favoriteword)
        self._session.flush()

    async def remove_favorite(self, word: str, user: UserSchema):
        word = self._session.scalar(select(Word).where(Word.text == word))
        delete(FavoriteWord).where(
            FavoriteWord.word_id == word.id,
            FavoriteWord.user_id == user.id,
        )
        self._session.commit()

    async def get_favorite(
        self,
        user: UserSchema,
        page_number: int,
    ) -> list[Word]:
        words = self._session.scalars(
            select(Word)
            .join(
                FavoriteWord,
                (Word.id == FavoriteWord.word_id) & (FavoriteWord.user_id == user.id),
            )
            .order_by(FavoriteWord.id)
            .offset(self.page_size * page_number)
            .limit(self.page_size),
        )
        return [word for word in words]


# SELECT words.id AS words_id, words.text AS words_text, words.language_id AS words_language_id, words_1.text AS "translateWord"
# FROM words
# JOIN wordtranslates ON words.id = wordtranslates.word_from_id OR words.id = wordtranslates.word_to_id
# JOIN words AS words_1 ON words_1.id = wordtranslates.word_from_id AND words.id = wordtranslates.word_from_id OR words.id = wordtranslates.word_from_id AND words_1.id = wordtranslates.word_from_id
# WHERE words.text = %(text_1)s


class QuizeFilter(BaseModel):
    user: UserSchema
    theme_id: int | None = None
    level: int | None = None
    max_question: int = 5

    def get_expression(self):
        expression = sa.true()
        if self.theme_id is not None:
            expression &= QuizQuestion.theme_id == self.theme_id
        if self.level is not None:
            expression &= QuizQuestion.level == self.level
        expression &= QuizQuestion.max_question == self.max_question
        return expression


class QuizeService:
    def __init__(self, session: Session) -> None:
        self._session = session

    async def get_game(
        self,
        user: UserSchema,
        quize_filter: QuizeFilter | None = None,
    ) -> Sequence[QuizQuestion]:
        quize_filter = quize_filter or QuizeFilter(user=user)
        params = quize_filter.get_expression()
        quizQuestions = list(self._session.query(QuizQuestion.id).where(params).all())
        if quizQuestions == []:
            return []
        selected_games = random.sample(
            quizQuestions,
            min(len(quizQuestions), quize_filter.max_question),
        )

        return (
            self._session.scalars(
                select(QuizQuestion).where(
                    QuizQuestion.id.in_([i.id for i in selected_games]),
                ),
            )
        ).all()

    async def get_filter_by_user(self, user: UserSchema) -> QuizeFilter:
        f = self._session.scalar(
            select(QuizeFilter).where(QuizeFilter.user.id == user.id)
        )
        if f:
            return f
        return QuizeFilter(user=user)

    async def get_quize_theme_by_id(self, theme_id) -> None | QuizTheme:
        return self._session.scalar(select(QuizTheme).where(QuizTheme.id == theme_id))

    async def get_quize_theme_by_name(self, theme_name) -> None | QuizTheme:
        return self._session.scalar(
            select(QuizTheme).where(QuizTheme.name == theme_name)
        )

    async def update_filter_data(self, user: UserSchema, values) -> None:
        self._session.execute(
            update(QuizeFilter).where(QuizeFilter.user.id == user.id).values(values)
        )
