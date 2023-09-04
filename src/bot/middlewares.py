import aioinject
from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class AIOInjectMiddleware(BaseMiddleware):
    def __init__(self, container: aioinject.Container) -> None:
        self._container = container

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self._container.context() as ctx:
            data["aioinject_context"] = ctx
            return await super().__call__(handler, event, data)
