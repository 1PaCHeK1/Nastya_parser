from contextlib import AbstractContextManager
from typing import Callable
from core.words.schemas import WordCreateSchema
from sqlalchemy.orm import Session
import bs4

from core.words.models import FavoriteWord


class WordService:
    def __init__(
        self, 
        session: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session = session

    async def get_translate(self, word: str) -> str:
        async with self.session.get(f"http://wooordhunt.ru/word/{word}", ssl=False) as response:
            body = bs4.BeautifulSoup(await response.text(), features="html.parser")
            translate = body.find("div", class_="t_inline_en") or body.find("p", class_="t_inline")
            translate = translate.text if translate is not None else "Перевод не найден"
            return translate

    async def get_phrases(self, word: str) -> str:
        async with self.session.get(f"http://wooordhunt.ru/word/{word}", ssl=False) as response:
            body = bs4.BeautifulSoup(await response.text(), features="html.parser")
            phrases = body.find("div", class_="block phrases")
            phrases = phrases.text if phrases is not None else "Фразы не найдены"
            return phrases

    async def get_examples(self, word: str) -> str:
        async with self.session.get(f"http://wooordhunt.ru/word/{word}", ssl=False) as response:
            body = bs4.BeautifulSoup(await response.text(), features="html.parser")
            examples = body.find_all("p", class_="ex_o")
            examples = '\n'.join([i.text for i in examples]) if examples is not [] else "Примеры не найдены"
            return examples

    async def append_word(self, word: WordCreateSchema):
        print("APPEND", word)

# redis -> db -> wooordhunt
