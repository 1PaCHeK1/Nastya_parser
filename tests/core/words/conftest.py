import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.words.schemas import WordCreateSchema
from core.words.services import WordService


@pytest.fixture
async def word(
    session: AsyncSession,
    word_service: WordService,
) -> WordCreateSchema:
    word = WordCreateSchema(
        word="hello",
        translate_words=[
            "Привет",
            "Здравствуй",
        ],
    )
    await word_service.append_word(word, session)
    return word
