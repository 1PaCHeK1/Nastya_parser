import asyncio
from typing import Any, Callable, Coroutine, TypeVar
import aiohttp
import bs4
import requests


class TranslateNotFoundException(Exception):
    ...


ReturnType = TypeVar("ReturnType")

def async_to_sync(
    callable_function: Callable[[], Coroutine[Any, Any, ReturnType]]
) -> ReturnType:  # type: ignore[return-value]
    loop = asyncio.get_event_loop()
    if loop.is_running():
        return loop.create_task(callable_function())
    else:
        return loop.run_until_complete(callable_function())


class TranslateWordService:

    def __init__(self) -> None:
        self.session = aiohttp.ClientSession()

    async def get_translate(self, word: str) -> list[str]:
        # async with self.session.get(f"http://wooordhunt.ru/word/{word}", ssl=False) as response:
        #     body = bs4.BeautifulSoup(await response.text(), features="html.parser")
        #     translate = body.find("div", class_="t_inline_en") or body.find("p", class_="t_inline")
        #     translate = translate.text if translate is not None else "Перевод не найден"
        #     return translate.split(", ")
        page = requests.get("http://wooordhunt.ru/word/" + word)
        if page.status_code == 200:
            soup = bs4.BeautifulSoup(page.text, 'html.parser')
            translations = soup.find('div', class_="t_inline_en") or soup.find('p', class_="t_inline")
            if translations:
                return translations.text.split(', ')
        # return []
        raise TranslateNotFoundException

    async def __aexit__(self):
        await self.close()

    def __del__(self):
        async_to_sync(self.close)

    async def close(self):
        await self.session.close()
