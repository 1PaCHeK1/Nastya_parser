from contextlib import AbstractContextManager
from typing import Callable
import sqlalchemy as sa
from sqlalchemy.orm import Session

from core.database import Database
from core.users.schemas import UserSchema
from core.words.schemas import WordCreateSchema
from core.caches.services import RedisService
from parsers.translate_word import TranslateWordService


from core.words.models import Word, FavoriteWord, WordTranslate

# redis -> database -> wooordhunt
class WordService:
    def __init__(
        self,
        parser_service: TranslateWordService,
        cache_service: RedisService,
    ) -> None:

        self.parser_service = parser_service
        self.cache_service = cache_service

    async def get_translate(self, user: UserSchema, word: str, session: Session) -> list[str]:
        print("find in redis")
        translate_words = None and await self.cache_service.get_translate(user, word)
        if translate_words:
            return translate_words

        print("find in database")
        TranslateWord = sa.orm.util.AliasedClass(Word)
        translate_words = (
            session
            .query(Word.text, TranslateWord.text.label("translate_word"))
            .join(WordTranslate,
                (Word.id==WordTranslate.word_from_id) | (Word.id==WordTranslate.word_to_id)
            )
            .join(TranslateWord,
                ((TranslateWord.id==WordTranslate.word_from_id) & (Word.id==WordTranslate.word_to_id))
                | ((Word.id==WordTranslate.word_from_id) & (TranslateWord.id==WordTranslate.word_to_id))
            )
            .where(Word.text==word)
            .all()
        )
        translate_words = [
            translate_word.translate_word
            for translate_word in translate_words
        ]

        if translate_words is None:
            print("find in site")
            translate_words = await self.parser_service.get_translate(word)


        await self.cache_service.set_translate(word, translate_words)
        return translate_words

    async def get_phrases(self, word: str) -> str:
        ...

    async def get_examples(self, word: str) -> str:
        ...

    async def append_word(self, word: WordCreateSchema):
        print("APPEND", word)

# SELECT words.id AS words_id, words.text AS words_text, words.language_id AS words_language_id, words_1.text AS "translateWord"
# FROM words
# JOIN wordtranslates ON words.id = wordtranslates.word_from_id OR words.id = wordtranslates.word_to_id
# JOIN words AS words_1 ON words_1.id = wordtranslates.word_from_id AND words.id = wordtranslates.word_from_id OR words.id = wordtranslates.word_from_id AND words_1.id = wordtranslates.word_from_id
# WHERE words.text = %(text_1)s