from sqlalchemy.orm import Session
from core.users.schemas import UserSchema
from core.words.schemas import WordCreateSchema
from core.words.services import WordService


async def test_get_word_from_db(
    word_service: WordService,
    user: UserSchema,
    word: WordCreateSchema,
    session: Session
):
    translated_words = await word_service.get_translate(
        user=user,
        word=word.word,
        session=session,
    )

    assert sorted(translated_words) == sorted([w.lower() for w in word.translate_words])


async def test_get_word_from_cache():
    pass
