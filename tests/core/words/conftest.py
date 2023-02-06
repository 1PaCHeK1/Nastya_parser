import pytest
from core.words.services import WordService
from core.words.schemas import WordCreateSchema


@pytest.fixture
async def word(word_service: WordService) -> WordCreateSchema:
    word = WordCreateSchema(
        word="hello",
        translate_words=[
            "Привет",
            "Здравствуй",
        ]
    )
    await word_service.append_word(word)
    return word
