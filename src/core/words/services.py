
import sqlalchemy as sa
from sqlalchemy.orm import Session

from pydantic import BaseModel
from core.users.schemas import UserSchema
from core.words.schemas import WordCreateSchema
from core.words.models import Word, Language, Translate
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

    async def append_word(self, word: WordCreateSchema, session: Session) -> None:
        russian_alphabet = [chr(i) for i in range(ord("а"), ord("я")+1)]
        english_alphabet = [chr(i) for i in range(ord("a"), ord("z")+1)]
        # ru en
        language_code = (
            "ru"
            if any(ru_symbol in word.word for ru_symbol in russian_alphabet) else
            "en"
        )
        russian, english = (
            session
            .query(Language)
            .where(Language.name.in_(["en", "ru"]))
            .order_by(Language.order)
            .all()
        )
        print(russian, english)
        main_word = Word(
            text=word.word,
            language_id=(
                russian.id if language_code == 'ru' else english.id
            )
        )
        session.add(main_word)
        session.flush()
        for word_translate in word.translate_words:
            translate = Word(
                text=word_translate,
                language_id=(russian.id if language_code == 'en' else english.id)
            )
            session.add(translate)
            session.flush()
            wordtranslate = WordTranslate(
                word_from_id=main_word.id,
                word_to_id=translate.id
            )
            session.add(wordtranslate)
            session.flush()


# SELECT words.id AS words_id, words.text AS words_text, words.language_id AS words_language_id, words_1.text AS "translateWord"
# FROM words
# JOIN wordtranslates ON words.id = wordtranslates.word_from_id OR words.id = wordtranslates.word_to_id
# JOIN words AS words_1 ON words_1.id = wordtranslates.word_from_id AND words.id = wordtranslates.word_from_id OR words.id = wordtranslates.word_from_id AND words_1.id = wordtranslates.word_from_id
# WHERE words.text = %(text_1)s

class QuizeFilter(BaseModel):
    user: UserSchema
    theme_id: int
    level: int
    max_question: int

    def get_expression(self):
        ...


class QuizeService:

    async def get_game(
        self,
        session: Session,
        quize_filter: QuizeFilter | None = None,
    ):
        params = quize_filter.get_expression()
